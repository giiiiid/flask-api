from flask import Flask
from flask_api.config import Config
from flask_api.utils import bcrypt, db
from flask_api.users.routes import users
from flask_jwt_extended import JWTManager
from flask_api.bookmarks.routes import bookmarks


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)
    
    app.register_blueprint(users)
    app.register_blueprint(bookmarks)

    JWTManager(app)

    db.init_app(app)
    bcrypt.init_app(app)
    return app