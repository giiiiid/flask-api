from flask import Flask
from flaskapi.config import Config
from flaskapi.main.routes import main
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)
    
    app.register_blueprint(main)

    db.init_app(app)
    return app