from flask import render_template, request, jsonify
from app.models import PythonProgram, TestCase, db
from app.sandbox.runner import run_code, test_code
from app.utils import load_new_challenges, extract_feedback
from app.code_styles import CODE_STYLES
import json, tomllib, os
import subprocess
import tempfile
import ast
import re
import sys


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
            inputs = data.get('input', [])

            # Ensure all inputs are strings
            inputs = [str(i) for i in inputs]

            # Execute the code using the sandbox runner
            result = run_code(code, inputs)
            return jsonify(result)
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    @app.route('/sandbox/test', methods=['POST'])
    def run_tests():
        try:
            data = request.get_json()
            program_id = data.get('program_id')
            code = data.get('code')
            style_key = data.get('style')  # Pass the style key from frontend

            program = PythonProgram.query.get_or_404(program_id)

            # Prepare test cases
            test_cases = [
                {
                    "name": tc.name,
                    "inputs": json.loads(tc.inputs),
                    "expected_output": tc.expected_output
                }
                for tc in program.test_cases
            ]

            # Test the code using the sandbox runner
            results = test_code(code, test_cases)

            # --- Integrate style check and scoring ---
            if style_key:
                final_score, combined_feedback = combine_test_and_style_results(
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
        return jsonify([{"id": p.id, "name": p.name, "description": p.description, "difficulty": p.difficulty} for p in programs])

    @app.route('/sandbox/load', methods=['GET'])
    def load_program():
        program_id = request.args.get('program_id')
        print(f"Requested program ID: {program_id}")  # Debugging
        program = PythonProgram.query.get(program_id)
        if not program:
            print("Program not found")  # Debugging
            return jsonify({"error": "Program not found"}), 404
        print(f"Program found: {program.name}")  # Debugging
        return jsonify({"id": program.id, "name": program.name, "code": program.code,
                        "max_lines": program.max_lines, "max_bytes": program.max_bytes})

    @app.route('/sandbox/save', methods=['POST'])
    def save_challenge():
        try:
            data = request.json
            print("Received data:", data)  # Debugging

            name = data.get('name')
            code = data.get('code')
            toml_content = data.get('toml')  # Get the TOML content from the frontend

            if not name or not code or not toml_content:
                return jsonify({"error": "Name, code, and TOML are required"}), 400

            # Parse the TOML content
            try:
                toml_data = tomllib.loads(toml_content)
                test_cases = toml_data.get('test_cases', [])
                description = toml_data.get('description')
                difficulty = toml_data.get('difficulty')
                max_lines = toml_data.get('max_lines')
                max_bytes = toml_data.get('max_bytes')
            except tomllib.TOMLDecodeError as e:
                print("Error parsing TOML:", str(e))
                return jsonify({"error": "Invalid TOML format"}), 400

            # Check if the program already exists
            program = PythonProgram.query.filter_by(name=name).first()

            if program:
                # Update the existing program's code
                print(f"Updating program: {name}")  # Debugging
                program.code = code
                program.description = description
                program.difficulty = difficulty
                program.max_lines = max_lines
                program.max_bytes = max_bytes
                db.session.commit()
            else:
                print(f"Creating new program: {name}")
                program = PythonProgram(name=name, code=code, description=description,
                                        difficulty=difficulty, max_lines=max_lines, max_bytes=max_bytes)
                db.session.add(program)
                db.session.commit()

            # Save the test cases
            for test_case in test_cases:
                inputs = test_case.get('inputs', [])
                expected_output = test_case.get('expected_output', '')

                # Ensure inputs are saved as valid JSON
                inputs_json = json.dumps(inputs)  # Convert inputs to JSON format

                # Check if the test case already exists for this program
                existing_test_case = TestCase.query.filter_by(
                    program_id=program.id, inputs=inputs_json
                ).first()

                if existing_test_case:
                    # Update the existing test case
                    print(f"Updating test case for inputs: {inputs}")  # Debugging
                    existing_test_case.expected_output = expected_output
                else:
                    # Add a new test case
                    print(f"Adding new test case for inputs: {inputs}")  # Debugging
                    db.session.add(TestCase(program_id=program.id, inputs=inputs_json, expected_output=expected_output))

            db.session.commit()

            return jsonify({"message": "Challenge saved successfully!"})
        except Exception as e:
            print("Error in save_challenge:", str(e))  # Debugging
            return jsonify({"error": "An error occurred while saving the challenge"}), 500

    @app.route('/sandbox/load-db', methods=['POST'])
    def load_db():
        load_new_challenges()
        return jsonify({"message": "Database updated with new challenges!"})

    @app.route('/sandbox/program/<program_name>', methods=['GET'])
    def get_program_code(program_name):
        try:
            # Locate the program file in the "challenges" directory
            program_path = os.path.join("challenges", f"{program_name}.py")
            if not os.path.exists(program_path):
                return jsonify({"error": "Program not found"}), 404

            # Read the program file
            with open(program_path, 'r', encoding='utf-8') as file:  # Ensure UTF-8 encoding
                content = file.read()

            # Extract the YAML metadata and code
            if "'''!SIX:" in content and "!SIX.'''" in content:
                metadata_start = content.find("'''!SIX:") + len("'''!SIX:")  # Start of the metadata block
                metadata_end = content.find("!SIX.'''", metadata_start)  # End of the metadata block
                if metadata_end == -1:
                    return jsonify({"error": "Malformed metadata block"}), 400  # Handle missing end marker

                toml_content = content[metadata_start:metadata_end].strip()
                print(f"TOML={toml_content}")
                code = content[metadata_end + len("!SIX.'''"):].strip()
            else:
                toml_content = None
                code = content.strip()

            # Parse the TOML metadata (if present)
            metadata = None
            if toml_content:
                try:
                    metadata = tomllib.loads(toml_content)
                except tomllib.TOMLDecodeError as e:
                    return jsonify({"error": f"Invalid TOML format: {str(e)}"}), 400

            return jsonify({"code": code, "metadata": metadata})
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    @app.route('/sandbox/test_cases/<int:program_id>', methods=['GET'])
    def get_test_cases(program_id):
        try:
            program = PythonProgram.query.get(program_id)
            if not program:
                return jsonify({"error": "Program not found"}), 404

            test_cases = [
                {
                    "number": tc.id,  # Use the test case ID or a sequential number
                    "name": tc.name,  # Include the name field
                    "inputs": json.loads(tc.inputs),
                    "expected_output": tc.expected_output
                }
                for tc in program.test_cases
            ]
            return jsonify(test_cases)
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    @app.route('/sandbox/original_code/<int:program_id>', methods=['GET'])
    def get_original_code(program_id):
        program = PythonProgram.query.get(program_id)  # Use PythonProgram instead of Program
        if not program:
            return jsonify({"error": "Program not found"}), 404

        return jsonify({"original_code": program.code})  # Return the program's code

    @app.route('/sandbox/styles', methods=['GET'])
    def get_code_styles():
        # Only send frontend-relevant fields
        frontend_fields = [
            "key", "name", "description", "code_version"
        ]
        styles = [
            {k: style[k] for k in frontend_fields}
            for style in CODE_STYLES
        ]
        return jsonify(styles)

    def run_pylint(code, pylint_args):
        with tempfile.NamedTemporaryFile('w', delete=False, suffix='.py', encoding='utf-8') as tmp:
            tmp.write(code)
            tmp_path = tmp.name
        try:
            cmd = [sys.executable, "-m", "pylint", tmp_path] + (pylint_args or [])
            result = subprocess.run(cmd, capture_output=True, text=True, encoding='utf-8')
            return result.stdout
        finally:
            import os
            os.unlink(tmp_path)

    def check_structured(code):
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

    def check_readable(code):
        issues = []
        lines = code.strip().split('\n')
        non_empty = [l for l in lines if l.strip()]

        # Comments
        comment_lines = [l for l in non_empty if l.strip().startswith('#')]
        if len(non_empty) > 3 and len(comment_lines) == 0:
            issues.append("no comments")

        # Magic numbers: numeric literals (other than 0 and 1) in expressions
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

        # Consistent indentation: base unit must be 2 or 4 spaces, all others multiples of it
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

    def check_robust(code):
        issues = []
        try:
            tree = ast.parse(code)

            has_input = any(
                isinstance(node, ast.Call) and getattr(node.func, 'id', '') == 'input'
                for node in ast.walk(tree)
            )

            if has_input:
                # Type conversion: int()/float()/str() used anywhere
                has_type_conversion = any(
                    isinstance(node, ast.Call) and getattr(node.func, 'id', '') in ('int', 'float', 'str')
                    for node in ast.walk(tree)
                )
                if not has_type_conversion:
                    issues.append("input not type-checked")

                # Validation: while loop containing input(), or any if/Compare in code
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

            # try/except: informational only, no penalty
            if any(isinstance(node, ast.Try) for node in ast.walk(tree)):
                issues.append("try/except found")

        except Exception:
            pass

        return ' '.join(issues) if issues else "robust OK"

    def check_oop(code):
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

            # Find variable names assigned by instantiating a class
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

            # Check that a method is called on one of those instances
            for node in ast.walk(tree):
                if isinstance(node, ast.Call):
                    if isinstance(node.func, ast.Attribute):
                        if isinstance(node.func.value, ast.Name):
                            if node.func.value.id in instance_names:
                                return "OOP OK"

            return "Class methods not used"
        except Exception:
            return "No class detected"

    def check_recursive(code):
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

            # Check that at least one recursive function is called from outside itself
            for node in ast.walk(tree):
                if isinstance(node, ast.Call) and isinstance(node.func, ast.Name):
                    if node.func.id in recursive_funcs:
                        # Verify the call is not inside the function itself (i.e. it's an external call)
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

    def check_minimalist(code, max_lines=None, max_bytes=None):
        issues = []
        try:
            tree = ast.parse(code)

            # Single-use variable detection
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

        # Line count check (ignore blank lines and comment-only lines)
        if max_lines is not None:
            code_lines = [l for l in code.splitlines() if l.strip() and not l.strip().startswith('#')]
            if len(code_lines) > max_lines:
                issues.append(f"Too many lines: {len(code_lines)} (max {max_lines})")

        # Byte count check
        if max_bytes is not None:
            byte_count = len(code.encode('utf-8'))
            if byte_count > max_bytes:
                issues.append(f"Too many bytes: {byte_count} (max {max_bytes})")

        return "; ".join(issues) if issues else "minimalist OK"

    def extract_pylint_score_and_feedback(pylint_output):
        # Extract score
        match = re.search(r'Your code has been rated at ([\d\.]+)/10', pylint_output)
        score = float(match.group(1)) if match else 0.0
        # Clamp to 1-10 scale (or 0-10 if you prefer)
        score = max(1, min(10, round(score)))
        # Feedback: show the full pylint output (or just the messages if you want)
        feedback = pylint_output
        return score, feedback

    def ast_score_and_feedback(ast_result, style):
        # For now, just 10 for True, 1 for False, and a message
        if style == "separation_of_concerns":
            if ast_result:
                return 10, "Separation of concerns: OK"
            else:
                return 1, "Separation of concerns: Needs improvement"
        elif style == "oop":
            if ast_result:
                return 10, "OOP Detected"
            else:
                return 1, "No class detected"
        elif style == "recursive":
            if ast_result:
                return 10, "Recursion Detected"
            else:
                return 1, "Code is not recursive"
        else:
            return 1, "No AST check implemented for this style."

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
        base_score = 10  # <-- Set base score to 0

        # Pylint check
        if style.get('pylint_required'):
            pylint_output = run_pylint(code, style.get('pylint_parameters'))
            feedback, score_delta = extract_feedback(
                pylint_output, style.get('pylint_feedback', [])
            )
            score = max(0, min(10, base_score + score_delta))
            results['pylint'] = {
                "score": score,
                "feedback": feedback or ["No major issues detected."]
            }

        # AST check
        if style.get('ast_required'):
            ast_check = style.get('ast_parameters', {}).get('check')
            if ast_check == "structured":
                ast_result = check_structured(code)
            elif ast_check == "readable":
                ast_result = check_readable(code)
            elif ast_check == "robust":
                ast_result = check_robust(code)
            elif ast_check == "oop":
                ast_result = check_oop(code)
            elif ast_check == "recursive":
                ast_result = check_recursive(code)
            elif ast_check == "minimalist":
                ast_result = check_minimalist(code, max_lines=max_lines, max_bytes=max_bytes)
            else:
                ast_result = ""
            feedback, score_delta = extract_feedback(
                ast_result, style.get('ast_feedback', [])
            )
            score = max(0, min(10, base_score + score_delta))
            results['ast'] = {
                "score": score,
                "feedback": feedback or [ast_result or "AST checks passed."]
            }

        return jsonify(results)

    # --- NEW: Utility to combine test and style results ---
    def combine_test_and_style_results(test_results, style_key, code, max_lines=None, max_bytes=None):
        # Get style config
        style = next((s for s in CODE_STYLES if s['key'] == style_key), None)
        base_score = 10

        # 1. Count failed tests and build test feedback
        failed_tests = 0
        test_feedback = []
        for test in test_results:
            if not test.get('passed', False):
                failed_tests += 1
                test_feedback.append(f"Test \"{test.get('name', test.get('number', ''))}\": Failed")
            else:
                test_feedback.append(f"Test \"{test.get('name', test.get('number', ''))}\": Passed")

        # 2. Run style check (pylint + ast)
        style_score = base_score
        style_feedback = []

        # Pylint
        if style and style.get('pylint_required'):
            pylint_output = run_pylint(code, style.get('pylint_parameters'))
            feedback, score_delta = extract_feedback(
                pylint_output, style.get('pylint_feedback', [])
            )
            style_score = max(0, min(style_score, base_score + score_delta))
            style_feedback.extend(feedback)

        # AST
        if style and style.get('ast_required'):
            ast_check = style.get('ast_parameters', {}).get('check')
            if ast_check == "structured":
                ast_result = check_structured(code)
            elif ast_check == "readable":
                ast_result = check_readable(code)
            elif ast_check == "robust":
                ast_result = check_robust(code)
            elif ast_check == "oop":
                ast_result = check_oop(code)
            elif ast_check == "recursive":
                ast_result = check_recursive(code)
            elif ast_check == "minimalist":
                ast_result = check_minimalist(code, max_lines=max_lines, max_bytes=max_bytes)
            else:
                ast_result = ""
            feedback, score_delta = extract_feedback(
                ast_result, style.get('ast_feedback', [])
            )
            style_score = max(0, min(style_score, base_score + score_delta))
            style_feedback.extend(feedback if feedback else [ast_result or "AST checks passed."])

        # 3. Subtract 2 for each failed test
        final_score = max(0, style_score - 2 * failed_tests)

        # 4. Combine feedback
        combined_feedback = []
        combined_feedback.append(f"Score: {final_score}/10")
        combined_feedback.extend(test_feedback)
        if style_feedback:
            combined_feedback.extend(style_feedback)

        return final_score, combined_feedback

    # ...rest of your routes...