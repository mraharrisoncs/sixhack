from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class PythonProgram(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    code = db.Column(db.Text, nullable=False)
    description = db.Column(db.String(200), nullable=True)
    difficulty = db.Column(db.String(20), nullable=True)
    topic = db.Column(db.String(50), nullable=True)
    spec_level = db.Column(db.String(20), nullable=True)
    hints = db.Column(db.Text, nullable=True)
    max_lines = db.Column(db.Integer, nullable=True)
    max_bytes = db.Column(db.Integer, nullable=True)
    solutions = db.Column(db.Text, nullable=True)
    test_cases = db.relationship('TestCase', backref='program', lazy=True)


class TestCase(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    program_id = db.Column(db.Integer, db.ForeignKey('python_program.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    inputs = db.Column(db.Text, nullable=False)
    expected_output = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return f"<TestCase {self.name}>"
