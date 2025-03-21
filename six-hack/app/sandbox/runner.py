import io
import contextlib
import traceback
import json
from app.models import PythonProgram, TestCase

def run_code(code, inputs):
    try:
        output = io.StringIO()
        input_iterator = iter(inputs)

        def mock_input(prompt=""):
            return next(input_iterator)

        with contextlib.redirect_stdout(output):
            exec(code, {"input": mock_input})

        return {"output": output.getvalue()}
    except Exception:
        return {"error": traceback.format_exc()}

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