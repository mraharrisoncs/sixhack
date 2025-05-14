from flask import render_template, request, jsonify
from app.models import PythonProgram, TestCase, db
from app.sandbox.runner import run_code, test_code
from app.utils import load_new_challenges
import json, yaml, os
import subprocess


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
            return jsonify({"results": results})
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    @app.route('/sandbox/programs', methods=['GET'])
    def get_programs():
        programs = PythonProgram.query.all()
        return jsonify([{"id": p.id, "name": p.name} for p in programs])

    @app.route('/sandbox/load', methods=['GET'])
    def load_program():
        program_id = request.args.get('program_id')
        print(f"Requested program ID: {program_id}")  # Debugging
        program = PythonProgram.query.get(program_id)
        if not program:
            print("Program not found")  # Debugging
            return jsonify({"error": "Program not found"}), 404
        print(f"Program found: {program.name}")  # Debugging
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

                yaml_content = content[metadata_start:metadata_end].strip()  # Extract YAML content
                print(f"YAML={yaml_content}")  # Debugging
                code = content[metadata_end + len("!SIX.'''"):].strip()  # Extract the code after the metadata block
            else:
                yaml_content = None
                code = content.strip()  # If no metadata block, return the entire content

            # Parse the YAML metadata (if present)
            metadata = None
            if yaml_content:
                try:
                    metadata = yaml.safe_load(yaml_content)  # Parse the YAML content
                except yaml.YAMLError as e:
                    return jsonify({"error": f"Invalid YAML format: {str(e)}"}), 400

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