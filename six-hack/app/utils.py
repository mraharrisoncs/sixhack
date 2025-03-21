import os
import ast
import json
from app.models import db, PythonProgram, TestCase

def parse_program_file(filepath):
    """Parse a program file to extract metadata and code."""
    with open(filepath, 'r') as file:
        lines = file.readlines()

    # Extract metadata from the top comment
    metadata = {}
    if lines[0].strip() == "'''!SIXHACK":
        for line in lines[1:]:
            if line.strip() == "'''":
                break
            key, value = line.split(':', 1)
            metadata[key.strip()] = ast.literal_eval(value.strip())

    # Extract the program code (after the metadata comment)
    code = ''.join(lines[len(metadata) + 2:])
    return metadata, code

def parse_test_cases(filepath):
    """Parse a JSON file to extract test cases."""
    with open(filepath, 'r') as file:
        return json.load(file)

def populate_database():
    """Clear the database and populate it with challenges and test cases."""
    # Clear existing data
    db.drop_all()
    db.create_all()

    # Load challenges from the "challenges" directory
    challenges_dir = os.path.join(os.path.dirname(__file__), '../challenges')
    for filename in os.listdir(challenges_dir):
        if filename.endswith('.py'):
            filepath = os.path.join(challenges_dir, filename)
            metadata, code = parse_program_file(filepath)

            # Add the program to the database
            program_name = filename.replace('.py', '')
            program = PythonProgram(name=program_name, code=code)
            db.session.add(program)
            db.session.commit()

            # Load test cases from the corresponding JSON file
            test_file = os.path.join(challenges_dir, f"{program_name}_tests.json")
            if os.path.exists(test_file):
                test_cases = parse_test_cases(test_file)
                for test_case in test_cases:
                    inputs = test_case.get('inputs', [])
                    expected_output = test_case.get('expected_output', '')
                    db.session.add(TestCase(program_id=program.id, inputs=str(inputs), expected_output=expected_output))
                db.session.commit()

    print("Database populated successfully!")