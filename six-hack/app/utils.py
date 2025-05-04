import os
import ast
import yaml  # Use PyYAML to parse the test cases
import json  # Import json for handling test case inputs and outputs
from app.models import db, PythonProgram, TestCase

def parse_program_file(filepath):
    """Parse a program file to extract metadata and code."""
    with open(filepath, 'r', encoding='utf-8') as file:
        content = file.read()

    if "'''!SIX:" in content and "!SIX.'''" in content:
        metadata_start = content.find("'''!SIX:") + len("'''!SIX:")
        metadata_end = content.find("!SIX.'''", metadata_start)
        yaml_content = content[metadata_start:metadata_end].strip()
        metadata = yaml.safe_load(yaml_content)
        code = content[metadata_end + len("!SIX.'''"):].strip()
    else:
        metadata = {}
        code = content.strip()

    return metadata, code

def parse_test_cases(filepath):
    """Parse a JSON file to extract test cases."""
    with open(filepath, 'r') as file:
        return json.load(file)

def populate_database():
    """Clear the database and populate it with challenges."""
    db.drop_all()
    db.create_all()

    challenges_dir = os.path.join(os.path.dirname(__file__), 'challenges')
    for filename in os.listdir(challenges_dir):
        if filename.endswith('.py'):
            filepath = os.path.join(challenges_dir, filename)
            metadata, code = parse_program_file(filepath)

            program = PythonProgram(name=filename.replace('.py', ''), code=code)
            db.session.add(program)
            db.session.commit()

            for test_case in metadata.get('test_cases', []):
                test_case_entry = TestCase(
                    program_id=program.id,
                    name=test_case.get('name', 'Unnamed Test Case'),  # Add the name field
                    inputs=json.dumps(test_case.get('inputs', [])),
                    expected_output=test_case.get('expected_output', '')
                )
                db.session.add(test_case_entry)

            db.session.commit()

    print("Database populated successfully!")

def load_new_challenges():
    """Load new challenges from the challenges directory and update the database."""
    challenges_dir = os.path.join(os.path.dirname(__file__), '../challenges')
    for filename in os.listdir(challenges_dir):
        if filename.endswith('.py'):
            filepath = os.path.join(challenges_dir, filename)
            metadata, code = parse_program_file(filepath)

            # Check if the program already exists
            program_name = filename.replace('.py', '')
            program = PythonProgram.query.filter_by(name=program_name).first()

            if program:
                # Update the existing program
                program.code = code
                db.session.commit()
            else:
                # Add a new program
                program = PythonProgram(name=program_name, code=code)
                db.session.add(program)
                db.session.commit()

            # Load or update test cases
            test_file = os.path.join(challenges_dir, f"{program_name}_tests.json")
            if os.path.exists(test_file):
                test_cases = parse_test_cases(test_file)
                for test_case in test_cases:
                    inputs = test_case.get('inputs', [])
                    expected_output = test_case.get('expected_output', '')

                    # Check if the test case already exists
                    existing_test_case = TestCase.query.filter_by(
                        program_id=program.id, inputs=str(inputs)
                    ).first()

                    if existing_test_case:
                        # Update the existing test case
                        existing_test_case.expected_output = expected_output
                        db.session.commit()
                    else:
                        # Add a new test case
                        db.session.add(TestCase(program_id=program.id, inputs=str(inputs), expected_output=expected_output))
                        db.session.commit()

    print("New challenges loaded successfully!")