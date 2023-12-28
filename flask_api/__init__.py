from flask import Flask, jsonify
from flask_api.config import Config
from flask_api.models import Bookmark
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


    @app.route("/<url>", methods=["GET"])
    def get_url_visits(url):
        watch_vid = Bookmark.query.filter_by(url=url).first_or_404()

        if watch_vid:
            watch_vid.visits = watch_vid.visits+1
            db.session.commit()
    
    
    @app.errorhandler(404)
    def error_404(e):
        return jsonify({"error":"Not found"}), 404
    

    return app