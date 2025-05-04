import os
import yaml  # Use YAML for parsing the metadata
import json  # Use JSON for storing test case inputs
from app import create_app
from app.models import db, PythonProgram, TestCase

app = create_app()

def parse_program_file(filepath):
    """Parse a program file to extract metadata and code."""
    with open(filepath, 'r') as file:
        content = file.read()

    # Extract YAML metadata from the top comment
    if "'''!SIX:" in content:
        yaml_start = content.find("'''!SIX:") + len("'''!SIX:")
        yaml_end = content.find("'''", yaml_start)
        yaml_content = content[yaml_start:yaml_end].strip()
        metadata = yaml.safe_load(yaml_content)  # Parse YAML
    else:
        metadata = {}

    # Extract the program code (after the metadata comment)
    code_start = content.find("'''", yaml_end + 3) + 3
    code = content[code_start:].strip()
    return metadata, code

with app.app_context():
    # Clear existing data
    db.drop_all()
    db.create_all()

    # Load programs from the "challenges" directory
    challenges_dir = os.path.join(os.path.dirname(__file__), 'challenges')
    for filename in os.listdir(challenges_dir):
        if filename.endswith('.py'):
            filepath = os.path.join(challenges_dir, filename)
            metadata, code = parse_program_file(filepath)

            # Add the program to the database
            program = PythonProgram(name=filename.replace('.py', ''), code=code)
            db.session.add(program)
            db.session.commit()

            # Add test cases to the database
            test_cases = metadata.get('test_cases', [])
            for test_case in test_cases:
                inputs = test_case.get('inputs', [])
                expected_output = test_case.get('expected_output', '')
                test_case_entry = TestCase(
                    program_id=program.id,
                    inputs=json.dumps(inputs),  # Store inputs as JSON
                    expected_output=expected_output
                )
                db.session.add(test_case_entry)

            db.session.commit()

    print("Database populated successfully!")