from flask import render_template, request, jsonify
from app.models import PythonProgram, TestCase
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