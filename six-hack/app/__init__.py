# filepath: /workspaces/six-hack/app/__init__.py
from flask import Flask
from .routes import setup_routes

def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')

    with app.app_context():
        setup_routes(app)  # Register routes
        return app