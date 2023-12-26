from flask import Blueprint, jsonify, json, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_api.models import Bookmark
from flask_api.utils import db
import validators

bookmarks = Blueprint("bookmarks", __name__)


@bookmarks.route("/bookmarks/create-list", methods=["GET","POST"])
@jwt_required()
def watch_list():
    current_user = get_jwt_identity()

    if request.method == "POST":
        title = request.json.get("title")
        url = request.json.get("url")

        if not validators.url(url):
            return jsonify({"error":"Url is not valid"})
        else:
            new_watchlist = Bookmark(title=title, url=url, user_id=current_user)
            db.session.add(new_watchlist)
            db.session.commit()

        return jsonify({
            "id":new_watchlist.id,
            "title":new_watchlist.title,
            "url":new_watchlist.url,
            "visits":new_watchlist.visits,
            "user":new_watchlist.user_id,
            "created":new_watchlist.created_at
        }), 201

    else:
        user_watchlist = Bookmark.query.filter_by(user_id=current_user)
        data = []
        
        for item in user_watchlist:
            data.append({
                "id":item.id,
                "title":item.title,
                "url":item.url,
                "visits":item.visits,
                "user":item.user_id,
                "created":item.created_at
            })
        
        if len(data) == 0:
            return jsonify("You have no watchlist")
        else:
            return jsonify({"watchlists":data}), 200


@bookmarks.route("/bookmarks/<int:id>", methods=["GET","POST"])
def get_watchlist(id):
    watch_vid = Bookmark.query.get_or_404(id)
    return jsonify({
            "id":watch_vid.id,
            "title":watch_vid.title,
            "url":watch_vid.url,
            "visits":watch_vid.visits,
            "user":watch_vid.user_id,
            "created":watch_vid.created_at
        }), 200