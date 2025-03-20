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
        code = request.json.get('code', '')
        result = run_code(code)
        return jsonify(result=result)