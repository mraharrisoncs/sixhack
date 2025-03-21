from flask import render_template, request, jsonify
from app.models import PythonProgram, TestCase, db
from app.sandbox.runner import run_code, test_code

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
        data = request.json
        program_id = data.get('program_id')
        result = test_code(program_id)
        return jsonify(result)

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
        data = request.json
        name = data.get('name')
        code = data.get('code')
        test_cases = data.get('test_cases', [])

        # Save the program
        program = PythonProgram(name=name, code=code)
        db.session.add(program)
        db.session.commit()

        # Save the test cases
        for test_case in test_cases:
            inputs = test_case.get('inputs', [])
            expected_output = test_case.get('expected_output', '')
            db.session.add(TestCase(program_id=program.id, inputs=str(inputs), expected_output=expected_output))
        db.session.commit()

        return jsonify({"message": "Challenge saved successfully!"})