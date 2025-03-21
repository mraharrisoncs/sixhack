from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from .models import db
from .routes import setup_routes

def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///sixhack.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    with app.app_context():
        setup_routes(app)  # Register routes
        db.create_all()  # Create tables if they don't exist
        return app