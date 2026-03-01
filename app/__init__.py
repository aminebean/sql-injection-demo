from flask import Flask
from .init_db import init_db

def create_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = "dev-key-change-later"
    app.config["DB_PATH"] = "instance/app.db"

    # Initialize DB + seed users
    init_db(app.config["DB_PATH"])

    @app.get("/")
    def home():
        return "SQL Injection Demo Running"

    return app
