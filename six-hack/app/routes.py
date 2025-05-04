from flask import render_template, request, jsonify
from app.models import PythonProgram, TestCase, db
from app.sandbox.runner import run_code, test_code
from app.utils import load_new_challenges
import json, yaml

def setup_routes(app):
    @app.route('/')
    def home():
        return render_template('home.html')

    @app.route('/about')
    def about():
        return render_template('about.html')

    @app.route('/sandbox/run', methods=['POST'])
    def run():
        data = request.json
        code = data.get('code', '')
        inputs = data.get('input', [])
        result = run_code(code, inputs)
        return jsonify(result)

    @app.route('/sandbox/test', methods=['POST'])
    def test():
        import json  # Ensure the json module is imported

        data = request.json
        program_id = data.get('program_id')
        current_code = data.get('code')  # Get the current code from the frontend

        if not program_id or not current_code:
            return jsonify({"error": "Program ID and code are required"}), 400

        program = PythonProgram.query.get(program_id)
        if not program:
            return jsonify({"error": "Program not found"}), 404

        results = []
        for test_case in program.test_cases:
            try:
                print(f"Processing test case: {test_case.inputs}")  # Debugging
                inputs = json.loads(test_case.inputs)  # Parse inputs from JSON
                expected_output = test_case.expected_output
                print(f"Inputs: {inputs}, Expected Output: {expected_output}")  # Debugging

                # Run the current code against the inputs
                result = run_code(current_code, inputs)
                print(f"Result: {result}")  # Debugging

                # Compare the actual output with the expected output
                passed = result.get("output", "").strip() == expected_output.strip()
                results.append({
                    "inputs": inputs,
                    "expected": expected_output,
                    "actual": result.get("output", ""),
                    "passed": passed
                })
            except Exception as e:
                print(f"Error processing test case: {e}")  # Debugging
                results.append({
                    "inputs": test_case.inputs,
                    "expected": test_case.expected_output,
                    "actual": "Error",
                    "passed": False
                })

        return jsonify({"results": results})

    @app.route('/sandbox/programs', methods=['GET'])
    def get_programs():
        programs = PythonProgram.query.all()
        return jsonify([{"id": p.id, "name": p.name} for p in programs])

    @app.route('/sandbox/load', methods=['GET'])
    def load_program():
        program_id = request.args.get('program_id')
        program = PythonProgram.query.get(program_id)
        if not program:
            return jsonify({"error": "Program not found"}), 404
        return jsonify({"id": program.id, "name": program.name, "code": program.code})

    @app.route('/sandbox/save', methods=['POST'])
    def save_challenge():
        try:
            data = request.json
            print("Received data:", data)  # Debugging

            name = data.get('name')
            code = data.get('code')
            yaml_content = data.get('yaml')  # Get the YAML content from the frontend

            if not name or not code or not yaml_content:
                return jsonify({"error": "Name, code, and YAML are required"}), 400

            # Parse the YAML content
            try:
                yaml_data = yaml.safe_load(yaml_content)
                test_cases = yaml_data.get('test_cases', [])
            except yaml.YAMLError as e:
                print("Error parsing YAML:", str(e))  # Debugging
                return jsonify({"error": "Invalid YAML format"}), 400

            # Check if the program already exists
            program = PythonProgram.query.filter_by(name=name).first()

            if program:
                # Update the existing program's code
                print(f"Updating program: {name}")  # Debugging
                program.code = code
                db.session.commit()
            else:
                # Create a new program
                print(f"Creating new program: {name}")  # Debugging
                program = PythonProgram(name=name, code=code)
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