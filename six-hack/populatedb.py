from app import create_app
from app.models import db, PythonProgram, TestCase

app = create_app()

with app.app_context():
    # Add a sample program
    program = PythonProgram(name="Addition Program", code="a = int(input())\nb = int(input())\nprint(a + b)")
    db.session.add(program)
    db.session.commit()

    # Add a test case for the program
    test_case = TestCase(program_id=program.id, inputs='[1, 2]', expected_output='3\n')
    db.session.add(test_case)
    db.session.commit()

    print("Database populated successfully!")