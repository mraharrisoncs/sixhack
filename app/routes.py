"""Route definitions for the Six Hack sandbox."""

import json
import os
import subprocess
import tempfile
import ast
import re
import sys

from flask import render_template, request, jsonify
from app.models import PythonProgram, TestCase, db
from app.sandbox.runner import run_code, test_code
from app.utils import extract_feedback
from app.code_styles import CODE_STYLES


def setup_routes(app):

    @app.route('/')
    def home():
        return render_template('home.html')

    @app.route('/about')
    def about():
        return render_template('about.html')

    @app.route('/sandbox/run', methods=['POST'])
    def run():
        try:
            data = request.json
            code = data.get('code', '')
            inputs = [str(i) for i in data.get('input', [])]
            return jsonify(run_code(code, inputs))
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    @app.route('/sandbox/test', methods=['POST'])
    def run_tests():
        try:
            data = request.get_json()
            program_id = data.get('program_id')
            code = data.get('code')
            style_key = data.get('style')

            program = PythonProgram.query.get_or_404(program_id)

            test_cases = [
                {
                    "name": tc.name,
                    "inputs": json.loads(tc.inputs),
                    "expected_output": tc.expected_output
                }
                for tc in program.test_cases
            ]

            results = test_code(code, test_cases)

            if style_key:
                final_score, combined_feedback = _combine_test_and_style_results(
                    results, style_key, code,
                    max_lines=program.max_lines, max_bytes=program.max_bytes
                )
            else:
                final_score = None
                combined_feedback = []

            return jsonify({
                "results": results,
                "score": final_score,
                "feedback": combined_feedback
            })
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    @app.route('/sandbox/programs', methods=['GET'])
    def get_programs():
        programs = PythonProgram.query.all()
        return jsonify([
            {"id": p.id, "name": p.name, "description": p.description,
             "difficulty": p.difficulty, "topic": p.topic, "spec_level": p.spec_level}
            for p in programs
        ])

    @app.route('/sandbox/load', methods=['GET'])
    def load_program():
        program_id = request.args.get('program_id')
        program = PythonProgram.query.get(program_id)
        if not program:
            return jsonify({"error": "Program not found"}), 404
        return jsonify({
            "id": program.id,
            "name": program.name,
            "code": program.code,
            "description": program.description,
            "topic": program.topic,
            "spec_level": program.spec_level,
            "hints": json.loads(program.hints or "[]"),
            "max_lines": program.max_lines,
            "max_bytes": program.max_bytes
        })

    @app.route('/sandbox/test_cases/<int:program_id>', methods=['GET'])
    def get_test_cases(program_id):
        try:
            program = PythonProgram.query.get(program_id)
            if not program:
                return jsonify({"error": "Program not found"}), 404
            return jsonify([
                {
                    "number": tc.id,
                    "name": tc.name,
                    "inputs": json.loads(tc.inputs),
                    "expected_output": tc.expected_output
                }
                for tc in program.test_cases
            ])
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    @app.route('/sandbox/original_code/<int:program_id>', methods=['GET'])
    def get_original_code(program_id):
        program = PythonProgram.query.get(program_id)
        if not program:
            return jsonify({"error": "Program not found"}), 404
        return jsonify({"original_code": program.code})

    @app.route('/sandbox/styles', methods=['GET'])
    def get_code_styles():
        frontend_fields = ["key", "name", "description", "code_version"]
        return jsonify([{k: style[k] for k in frontend_fields} for style in CODE_STYLES])

    @app.route('/sandbox/style_check', methods=['POST'])
    def style_check():
        data = request.get_json()
        style_key = data.get('style')
        code = data.get('code')
        max_lines = data.get('max_lines')
        max_bytes = data.get('max_bytes')
        style = next((s for s in CODE_STYLES if s['key'] == style_key), None)
        if not style:
            return jsonify({"error": "Unknown style"}), 400

        results = {}
        base_score = 10

        if style.get('pylint_required'):
            pylint_output = _run_pylint(code, style.get('pylint_parameters'))
            feedback, score_delta = extract_feedback(pylint_output, style.get('pylint_feedback', []))
            results['pylint'] = {
                "score": max(0, min(10, base_score + score_delta)),
                "feedback": feedback or ["No major issues detected."]
            }

        if style.get('ast_required'):
            ast_result = _run_ast_check(style, code, max_lines, max_bytes)
            feedback, score_delta = extract_feedback(ast_result, style.get('ast_feedback', []))
            results['ast'] = {
                "score": max(0, min(10, base_score + score_delta)),
                "feedback": feedback or [ast_result or "AST checks passed."]
            }

        return jsonify(results)

    # ── Internal helpers ─────────────────────────────────────────────────────

    def _run_pylint(code, pylint_args):
        """Run pylint on code in a temp file and return its stdout."""
        with tempfile.NamedTemporaryFile('w', delete=False, suffix='.py', encoding='utf-8') as tmp:
            tmp.write(code)
            tmp_path = tmp.name
        try:
            cmd = [sys.executable, "-m", "pylint", tmp_path] + (pylint_args or [])
            result = subprocess.run(cmd, capture_output=True, text=True, encoding='utf-8')
            return result.stdout
        finally:
            os.unlink(tmp_path)

    def _run_ast_check(style, code, max_lines=None, max_bytes=None):
        """Dispatch to the appropriate AST checker for the given style."""
        check = style.get('ast_parameters', {}).get('check')
        dispatch = {
            "structured": lambda: _check_structured(code),
            "readable":   lambda: _check_readable(code),
            "robust":     lambda: _check_robust(code),
            "oop":        lambda: _check_oop(code),
            "recursive":  lambda: _check_recursive(code),
            "minimalist": lambda: _check_minimalist(code, max_lines=max_lines, max_bytes=max_bytes),
        }
        return dispatch[check]() if check in dispatch else ""

    def _check_structured(code):
        try:
            tree = ast.parse(code)
            has_function = any(isinstance(node, ast.FunctionDef) for node in tree.body)
            if not has_function:
                return "no function not separated"
            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef):
                    has_input = any(isinstance(n, ast.Call) and getattr(n.func, 'id', '') == 'input' for n in ast.walk(node))
                    has_output = any(isinstance(n, ast.Call) and getattr(n.func, 'id', '') == 'print' for n in ast.walk(node))
                    has_computation = any(isinstance(n, ast.BinOp) for n in ast.walk(node))
                    if (has_input and has_output) or (has_input and has_computation) or (has_output and has_computation):
                        return "not separated"
            return "structured OK"
        except Exception:
            return "no function"

    def _check_readable(code):
        issues = []
        lines = code.strip().split('\n')
        non_empty = [l for l in lines if l.strip()]
        comment_lines = [l for l in non_empty if l.strip().startswith('#')]

        if len(non_empty) > 3 and not comment_lines:
            issues.append("no comments")

        try:
            tree = ast.parse(code)
            for node in ast.walk(tree):
                if isinstance(node, (ast.Compare, ast.BinOp, ast.AugAssign)):
                    for child in ast.walk(node):
                        if isinstance(child, ast.Constant) and isinstance(child.value, (int, float)):
                            if child.value not in (0, 1, -1):
                                issues.append("magic number found")
                                break
                    else:
                        continue
                    break
        except Exception:
            pass

        indent_amounts = []
        for line in lines:
            stripped = line.lstrip(' ')
            if stripped and stripped != line and not stripped.startswith('#'):
                indent = len(line) - len(stripped)
                if indent > 0:
                    indent_amounts.append(indent)
        if indent_amounts:
            min_indent = min(indent_amounts)
            if min_indent not in (2, 4) or any(i % min_indent != 0 for i in indent_amounts):
                issues.append("inconsistent indentation")

        return ' '.join(issues) if issues else "readable OK"

    def _check_robust(code):
        issues = []
        try:
            tree = ast.parse(code)
            has_input = any(
                isinstance(node, ast.Call) and getattr(node.func, 'id', '') == 'input'
                for node in ast.walk(tree)
            )
            if has_input:
                has_type_conversion = any(
                    isinstance(node, ast.Call) and getattr(node.func, 'id', '') in ('int', 'float', 'str')
                    for node in ast.walk(tree)
                )
                if not has_type_conversion:
                    issues.append("input not type-checked")

                has_validation = False
                for node in ast.walk(tree):
                    if isinstance(node, ast.While):
                        if any(isinstance(n, ast.Call) and getattr(n.func, 'id', '') == 'input'
                               for n in ast.walk(node)):
                            has_validation = True
                            break
                    if isinstance(node, ast.If) and isinstance(node.test, ast.Compare):
                        has_validation = True
                        break
                if not has_validation:
                    issues.append("input not validated")

            if any(isinstance(node, ast.Try) for node in ast.walk(tree)):
                issues.append("try/except found")
        except Exception:
            pass
        return ' '.join(issues) if issues else "robust OK"

    def _check_oop(code):
        try:
            tree = ast.parse(code)
            class_defs = [node for node in ast.walk(tree) if isinstance(node, ast.ClassDef)]
            if not class_defs:
                return "No class detected"
            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef):
                    if node.args.args and node.args.args[0].arg != "self":
                        return "Method missing 'self'"
            class_names = {cls.name for cls in class_defs}
            instance_names = set()
            for node in ast.walk(tree):
                if isinstance(node, ast.Assign):
                    if isinstance(node.value, ast.Call) and isinstance(node.value.func, ast.Name):
                        if node.value.func.id in class_names:
                            for target in node.targets:
                                if isinstance(target, ast.Name):
                                    instance_names.add(target.id)
            if not instance_names:
                return "Class not instantiated"
            for node in ast.walk(tree):
                if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute):
                    if isinstance(node.func.value, ast.Name) and node.func.value.id in instance_names:
                        return "OOP OK"
            return "Class methods not used"
        except Exception:
            return "No class detected"

    def _check_recursive(code):
        try:
            tree = ast.parse(code)
            recursive_funcs = set()
            base_case_funcs = set()
            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef):
                    if any(isinstance(n, ast.Call) and getattr(n.func, 'id', '') == node.name for n in ast.walk(node)):
                        recursive_funcs.add(node.name)
                        if any(isinstance(n, ast.If) for n in ast.walk(node)):
                            base_case_funcs.add(node.name)
            if not recursive_funcs:
                return "No recursion detected"
            if not recursive_funcs.issubset(base_case_funcs):
                return "No base case detected"
            for node in ast.walk(tree):
                if isinstance(node, ast.Call) and isinstance(node.func, ast.Name):
                    if node.func.id in recursive_funcs:
                        # Verify the call is external (not inside the function itself)
                        called_externally = True
                        for func_node in ast.walk(tree):
                            if isinstance(func_node, ast.FunctionDef) and func_node.name == node.func.id:
                                if node in ast.walk(func_node):
                                    called_externally = False
                                    break
                        if called_externally:
                            return "Recursion OK"
            return "Recursive function never called"
        except Exception:
            return "No recursion detected"

    def _check_minimalist(code, max_lines=None, max_bytes=None):
        issues = []
        try:
            tree = ast.parse(code)
            assigned = {}
            for node in ast.walk(tree):
                if isinstance(node, ast.Assign):
                    for target in node.targets:
                        if isinstance(target, ast.Name):
                            assigned[target.id] = 0
            for node in ast.walk(tree):
                if isinstance(node, ast.Name) and isinstance(node.ctx, ast.Load):
                    if node.id in assigned:
                        assigned[node.id] += 1
            single_use = [name for name, count in assigned.items() if count == 1]
            if single_use:
                issues.append(f"Single-use variables could be inlined: {', '.join(single_use)}")
        except Exception:
            pass

        if max_lines is not None:
            code_lines = [l for l in code.splitlines() if l.strip() and not l.strip().startswith('#')]
            if len(code_lines) > max_lines:
                issues.append(f"Too many lines: {len(code_lines)} (max {max_lines})")

        if max_bytes is not None:
            byte_count = len(code.encode('utf-8'))
            if byte_count > max_bytes:
                issues.append(f"Too many bytes: {byte_count} (max {max_bytes})")

        return "; ".join(issues) if issues else "minimalist OK"

    def _combine_test_and_style_results(test_results, style_key, code, max_lines=None, max_bytes=None):
        """
        Combines functional test results with style analysis into a final score and feedback list.
        Deducts 2 points per failed test from the style score.
        """
        style = next((s for s in CODE_STYLES if s['key'] == style_key), None)
        base_score = 10

        # 1. Count failed tests and build per-test feedback
        failed_tests = 0
        test_feedback = []
        for test in test_results:
            if not test.get('passed', False):
                failed_tests += 1
                test_feedback.append(f"Test \"{test.get('name', test.get('number', ''))}\": Failed")
            else:
                test_feedback.append(f"Test \"{test.get('name', test.get('number', ''))}\": Passed")

        # 2. Run style checks (pylint + AST)
        style_score = base_score
        style_feedback = []

        if style and style.get('pylint_required'):
            pylint_output = _run_pylint(code, style.get('pylint_parameters'))
            feedback, score_delta = extract_feedback(pylint_output, style.get('pylint_feedback', []))
            style_score = max(0, min(style_score, base_score + score_delta))
            style_feedback.extend(feedback)

        if style and style.get('ast_required'):
            ast_result = _run_ast_check(style, code, max_lines, max_bytes)
            feedback, score_delta = extract_feedback(ast_result, style.get('ast_feedback', []))
            style_score = max(0, min(style_score, base_score + score_delta))
            style_feedback.extend(feedback if feedback else [ast_result or "AST checks passed."])

        # 3. Deduct 2 points per failed test
        final_score = max(0, style_score - 2 * failed_tests)

        # 4. Assemble combined feedback
        combined_feedback = [f"Score: {final_score}/10"] + test_feedback
        if style_feedback:
            combined_feedback.extend(style_feedback)

        return final_score, combined_feedback
