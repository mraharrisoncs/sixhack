import io
import contextlib
import traceback
import json
import subprocess
import tempfile
from app.models import PythonProgram, TestCase

def run_code(code, inputs):
    try:
        # Create a temporary file for the code
        with tempfile.NamedTemporaryFile(suffix='.py', delete=False) as temp_code_file:
            temp_code_file.write(code.encode('utf-8'))
            temp_code_path = temp_code_file.name

        # Run the code using subprocess
        process = subprocess.run(
            ['python', temp_code_path],
            input='\n'.join(inputs).encode('utf-8'),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=5  # Limit execution time to 5 seconds
        )

        # Return the output and errors
        return {
            "output": process.stdout.decode('utf-8'),
            "error": process.stderr.decode('utf-8')
        }
    except subprocess.TimeoutExpired:
        return {"error": "Execution timed out"}
    except Exception as e:
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