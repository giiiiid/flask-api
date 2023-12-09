from flask import Flask
from flaskapi.config import Config
from flaskapi.users.routes import users
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

# utils  configuration
db = SQLAlchemy()
bcrypt = Bcrypt()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)
    
    app.register_blueprint(users)

    db.init_app(app)
    bcrypt.init_app(app)
    return app