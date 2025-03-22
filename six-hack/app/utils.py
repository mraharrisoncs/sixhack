import os
import ast
import yaml  # Use PyYAML to parse the test cases
from app.models import db, PythonProgram, TestCase

def parse_program_file(filepath):
    """Parse a program file to extract metadata and code."""
    with open(filepath, 'r') as file:
        lines = file.readlines()

    # Extract metadata from the top comment
    metadata = {}
    code_start_index = 0
    if lines[0].strip() == "'''!SIX:":
        comment_block = []
        for i, line in enumerate(lines[1:], start=1):
            if line.strip() == "'''":
                code_start_index = i + 1  # Code starts after the closing triple quotes
                break
            comment_block.append(line)
        metadata = yaml.safe_load(''.join(comment_block))

    # Extract the program code (after the metadata comment)
    code = ''.join(lines[code_start_index:])
    return metadata, code

def parse_test_cases(filepath):
    """Parse a JSON file to extract test cases."""
    with open(filepath, 'r') as file:
        return json.load(file)

def populate_database():
    """Clear the database and populate it with challenges."""
    db.drop_all()
    db.create_all()

    challenges_dir = os.path.join(os.path.dirname(__file__), '../challenges')
    for filename in os.listdir(challenges_dir):
        if filename.endswith('.py'):
            filepath = os.path.join(challenges_dir, filename)
            metadata, code = parse_program_file(filepath)

            # Add the program to the database
            program = PythonProgram(name=filename.replace('.py', ''), code=code)
            db.session.add(program)
            db.session.commit()

            # Add test cases to the database
            for test_case in metadata.get('test_cases', []):
                inputs = test_case.get('inputs', [])
                expected_output = test_case.get('expected_output', '')
                db.session.add(TestCase(program_id=program.id, inputs=str(inputs), expected_output=expected_output))
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