import subprocess

def run_code(code, inputs):
    """
    Executes the given Python code with the provided inputs.
    :param code: The Python code to execute as a string.
    :param inputs: A list of inputs to provide to the code.
    :return: A dictionary containing the output or error.
    """
    try:
        # Join the inputs with newlines to simulate stdin
        input_data = "\n".join(map(str, inputs))

        # Use subprocess to execute the code
        process = subprocess.run(
            ["python", "-c", code],
            input=input_data,
            text=True,
            capture_output=True,
            check=True
        )

        # Return the standard output
        return {"output": process.stdout.strip()}
    except subprocess.CalledProcessError as e:
        # Handle errors during code execution
        return {"error": e.stderr.strip()}

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
            "expected": expected_output,
            "actual": actual_output,
            "passed": passed,
            "error": result.get("error", None)
        })

    return results