import io
import contextlib
import traceback

def run_code(code, inputs):
    try:
        # Create a StringIO object to capture print output
        output = io.StringIO()

        # Create an iterator for the input values
        input_iterator = iter(inputs)

        # Override the built-in input() function
        def mock_input(prompt=""):
            return next(input_iterator)

        # Redirect stdout to the StringIO object
        with contextlib.redirect_stdout(output):
            exec(code, {"input": mock_input})

        # Return only the captured output
        return {"output": output.getvalue()}
    except Exception:
        # Capture the full traceback and return it as the error message
        error_message = traceback.format_exc()
        return {"error": error_message}