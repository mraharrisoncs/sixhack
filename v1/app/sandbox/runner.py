import subprocess
import os
import sys

def _clean_env():
    """Return environment with debugpy/pydevd injection stripped out."""
    env = os.environ.copy()
    # Remove vars that cause debugpy to attach to subprocesses
    for key in list(env.keys()):
        if key.startswith(('PYDEVD', 'DEBUGPY', 'PYCHARM')):
            del env[key]
    # Strip debugpy paths from PYTHONPATH
    if 'PYTHONPATH' in env:
        paths = env['PYTHONPATH'].split(os.pathsep)
        paths = [p for p in paths if 'debugpy' not in p.lower() and 'pydevd' not in p.lower()]
        env['PYTHONPATH'] = os.pathsep.join(paths)
    env['PYTHONIOENCODING'] = 'utf-8'
    return env

def run_code(code, inputs):
    """
    Executes the given Python code with the provided inputs.
    :param code: The Python code to execute as a string.
    :param inputs: A list of inputs to provide to the code.
    :return: A dictionary containing the output or error.
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

        return {"output": process.stdout.decode('utf-8', errors='replace').strip()}
    except subprocess.CalledProcessError as e:
        stderr = e.stderr.strip()
        if "EOFError" in stderr:
            return {"error": "Ran out of inputs — check your test case supplies enough values."}
        return {"error": stderr}

def test_code(code, test_cases):
    """
    Tests the given Python code against a list of test cases.
    :param code: The Python code to execute as a string.
    :param test_cases: A list of test cases, where each test case is a dictionary
                       with 'inputs' and 'expected_output'.
    :return: A list of results for each test case.
    """
    results = []
    for test_case in test_cases:
        inputs = test_case.get("inputs", [])
        expected_output = test_case.get("expected_output", "").strip()

        # Run the code with the given inputs
        result = run_code(code, inputs)

        # Compare the actual output with the expected output
        actual_output = result.get("output", "").strip()
        passed = actual_output == expected_output

        results.append({
            "name": test_case.get("name", "Unnamed Test"),
            "inputs": inputs,
            "expected_output": expected_output,
            "actual_output": actual_output,
            "passed": passed,
            "error": result.get("error", None)
        })

    return results