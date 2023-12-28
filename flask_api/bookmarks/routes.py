import validators
from flask_api.utils import db
from flask_api.models import Bookmark
from flask import Blueprint, jsonify, json, request, abort
from flask_jwt_extended import jwt_required, get_jwt_identity


bookmarks = Blueprint("bookmarks", __name__)


@bookmarks.route("/bookmarks/create-list", methods=["GET","POST"])
@jwt_required()
def create_view_watchlist():
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
        page = request.args.get("page", 1, type=int)
        user_watchlist = Bookmark.query.order_by(Bookmark.created_at).paginate(page=page, per_page=3)
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
@jwt_required()
def retrieve_watchlist(id):
    # current_user = get_jwt_identity()
    # watch_vid = Bookmark.query.filter_by(id=id, user_id=current_user).first()
    watch_vid = Bookmark.query.get_or_404(id)

    if not watch_vid:
        return jsonify({"message":"Video not found"}), 404
    
    return jsonify({
            "id":watch_vid.id,
            "title":watch_vid.title,
            "url":watch_vid.url,
            "visits":watch_vid.visits,
            "user":watch_vid.user_id,
            "created":watch_vid.created_at,
            "user":{
                "username":watch_vid.user.username,
            }
        }), 200


@bookmarks.route("/bookmarks/<int:id>/update", methods=["GET","PUT"])
@jwt_required()
def update_watchlist(id):
    current_user = get_jwt_identity()
    watch_vid = Bookmark.query.filter_by(id=id, user_id=current_user).first()

    if not watch_vid:
        return jsonify({"message":"Video not found"}), 404
    
    if request.method == "GET":
        return jsonify({
            "id":watch_vid.id,
            "title":watch_vid.title,
            "url":watch_vid.url,
            "visits":watch_vid.visits,
            "user":watch_vid.user_id,
            "created":watch_vid.created_at,
            "user":{
                "username":watch_vid.user.username,
            }
        }), 200

    elif request.method == "PUT":
        title = request.json.get("title")
        url = request.json.get("url")

        if not validators.url(url):
            return jsonify({"error":"Url is not valid"}), 400
        else:
            watch_vid.title = title
            watch_vid.url = url
            db.session.commit()

        return jsonify({
            "id":watch_vid.id,
            "title":watch_vid.title,
            "url":watch_vid.url,
            "visits":watch_vid.visits,
            "user":watch_vid.user_id,
            "updated":watch_vid.updated_at,
            "user":{
                "username":watch_vid.user.username,
            }
        }), 200
    

@bookmarks.route("/bookmarks/<int:id>/delete", methods=["GET","POST"])
@jwt_required()
def delete_watchlist(id):
    current_user = get_jwt_identity()
    watch_vid = Bookmark.query.get_or_404(id)

    if watch_vid.user_id != current_user:
        abort(403)

    if not watch_vid:
        return jsonify({"message":"Video not found"}), 404
    
    if request.method == "POST":
        db.session.delete(watch_vid)
        db.session.commit()
        return jsonify({"message":"Video is deleted"}), 200
