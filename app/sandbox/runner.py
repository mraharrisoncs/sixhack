"""Sandboxed Python code execution."""

import subprocess
import os
import sys


def _clean_env():
    """Return a copy of the environment with debugpy/pydevd injection stripped out."""
    env = os.environ.copy()
    for key in list(env.keys()):
        if key.startswith(('PYDEVD', 'DEBUGPY', 'PYCHARM')):
            del env[key]
    if 'PYTHONPATH' in env:
        paths = env['PYTHONPATH'].split(os.pathsep)
        env['PYTHONPATH'] = os.pathsep.join(
            p for p in paths if 'debugpy' not in p.lower() and 'pydevd' not in p.lower()
        )
    env['PYTHONIOENCODING'] = 'utf-8'
    return env


def run_code(code, inputs):
    """
    Execute Python code in a subprocess with the given inputs fed via stdin.

    Args:
        code: Python source code as a string.
        inputs: List of input values (converted to strings and newline-joined).

    Returns:
        Dict with 'output' on success or 'error' on failure.
    """
    try:
        input_bytes = "\n".join(map(str, inputs)).encode('utf-8')
        process = subprocess.run(
            [sys.executable, "-E", "-X", "utf8", "-c", code],
            input=input_bytes,
            capture_output=True,
            env=_clean_env()
        )
        if process.returncode != 0:
            stderr = process.stderr.decode('utf-8', errors='replace').strip()
            if "EOFError" in stderr:
                return {"error": "Ran out of inputs — check your test case supplies enough values."}
            return {"error": stderr}
        return {"output": process.stdout.decode('utf-8', errors='replace').replace('\r\n', '\n').strip()}
    except subprocess.CalledProcessError as e:
        stderr = e.stderr.strip()
        if "EOFError" in stderr:
            return {"error": "Ran out of inputs — check your test case supplies enough values."}
        return {"error": stderr}


def test_code(code, test_cases):
    """
    Run code against a list of test cases and return pass/fail results.

    Args:
        code: Python source code as a string.
        test_cases: List of dicts with 'inputs' and 'expected_output'.

    Returns:
        List of result dicts, one per test case.
    """
    results = []
    for test_case in test_cases:
        inputs = test_case.get("inputs", [])
        expected_output = test_case.get("expected_output", "").strip()
        result = run_code(code, inputs)
        actual_output = result.get("output", "").strip()
        results.append({
            "name": test_case.get("name", "Unnamed Test"),
            "inputs": inputs,
            "expected_output": expected_output,
            "actual_output": actual_output,
            "passed": actual_output == expected_output,
            "error": result.get("error")
        })
    return results
