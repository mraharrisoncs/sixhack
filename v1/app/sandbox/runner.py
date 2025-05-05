import io
import contextlib
import traceback
import json
import subprocess
import tempfile
import os
from app.models import PythonProgram, TestCase

def execute_code_in_sandbox(code, input_data):
    try:
        # Create a temporary file to store the code
        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as temp_code_file:
            temp_code_file.write(code)
            temp_code_path = temp_code_file.name

        # Use subprocess to execute the code
        process = subprocess.run(
            ["python", temp_code_path],  # Run the temporary Python file
            input=input_data,           # Pass the inputs as stdin
            text=True,                  # Enable text mode for input/output
            capture_output=True,        # Capture stdout and stderr
            timeout=5                   # Set a timeout to prevent infinite loops
        )

        # Clean up the temporary file
        try:
            os.remove(temp_code_path)
        except Exception as cleanup_error:
            print(f"Error cleaning up temporary file: {cleanup_error}")

        # Check for errors
        if process.returncode != 0:
            return process.stderr.strip()  # Return error output

        # Return the standard output
        return process.stdout.strip()
    except subprocess.TimeoutExpired:
        return "Error: Code execution timed out"
    except Exception as e:
        return f"Error: {str(e)}"

def run_code(code, inputs):
    try:
        print(f"Running code:\n{code}")  # Debugging
        print(f"With inputs: {inputs}")  # Debugging

        # Simulate running the code (replace this with actual sandbox logic)
        input_data = "\n".join(map(str, inputs))  # Join inputs with newlines
        print(f"Input data passed to sandbox: {input_data}")  # Debugging

        # Replace this with actual sandbox execution logic
        output = execute_code_in_sandbox(code, input_data)  # Replace with actual execution logic

        print(f"Output from sandbox: {output}")  # Debugging
        return {"output": output}
    except Exception as e:
        print(f"Error in run_code: {e}")  # Debugging
        return {"error": str(e)}

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