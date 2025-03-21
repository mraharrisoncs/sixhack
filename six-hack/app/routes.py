from flask import render_template, request, jsonify
from app.sandbox.runner import run_code

def setup_routes(app):
    @app.route('/')
    def home():
        return render_template('home.html')

    @app.route('/about')
    def about():
        return render_template('about.html')

    @app.route('/sandbox', methods=['POST'])
    def sandbox():
        data = request.json
        code = data.get('code', '')
        inputs = data.get('input', [])
        result = run_code(code, inputs)
        return jsonify(result)