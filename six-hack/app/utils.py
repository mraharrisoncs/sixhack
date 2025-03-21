import os
import ast
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

def populate_database():
    """Clear the database and populate it with challenges from the challenges directory."""
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
            program = PythonProgram(name=filename.replace('.py', ''), code=code)
            db.session.add(program)
            db.session.commit()

            # Add test cases to the database
            inputs = metadata.get('inputs', [])
            expected_output = metadata.get('expected_output', '')
            test_case = TestCase(program_id=program.id, inputs=str(inputs), expected_output=str(expected_output))
            db.session.add(test_case)
            db.session.commit()

    print("Database populated successfully!")