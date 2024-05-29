# app/__init__.py
from flask import Flask
from flask_cors import CORS
from app.config import Config

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # CORS 등록
    CORS(app)

    with app.app_context():
        from app import routes
        app.register_blueprint(routes.bp)

    return app