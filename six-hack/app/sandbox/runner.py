import io
import contextlib
import traceback
import json
import subprocess
from app.models import PythonProgram, TestCase

def run_code(code, inputs):
    try:
        print(f"Running code:\n{code}")  # Debugging
        print(f"With inputs: {inputs}")  # Debugging

        # Prepare the input as a string
        input_str = "\n".join(map(str, inputs))
        print(f"Input string: {input_str}")  # Debugging

        # Run the code in a subprocess
        process = subprocess.run(
            ["python3", "-c", code],
            input=input_str,
            text=True,
            capture_output=True,
            timeout=5
        )

        # Capture the output and errors
        output = process.stdout
        error = process.stderr
        print(f"Output: {output}, Error: {error}")  # Debugging

        return {"output": output, "error": error}
    except Exception as e:
        print(f"Error running code: {e}")  # Debugging
        return {"output": "", "error": str(e)}

def test_code(program_id):
    program = PythonProgram.query.get(program_id)
    if not program:
        return {"error": "Program not found"}

    results = []
    for test_case in program.test_cases:
        inputs = json.loads(test_case.inputs)
        expected_output = test_case.expected_output
        result = run_code(program.code, inputs)
        passed = result.get("output", "").strip() == expected_output.strip()
        results.append({"inputs": inputs, "expected": expected_output, "actual": result.get("output", ""), "passed": passed})

    return {"results": results}