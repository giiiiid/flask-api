from flask_api.utils import bcrypt, db
from flask_api.models import User, Bookmark
from flask import Blueprint, request, jsonify, json
from flask_jwt_extended import create_refresh_token, create_access_token, jwt_required, get_jwt_identity


users = Blueprint("users", __name__)


@users.route("/user/register", methods=["GET", "POST"])
def register():

    username = request.json.get("username")
    email = request.json.get("email")
    password = request.json.get("password")
    
    if len(username) and len(email) and len(password) < 3:
        return jsonify({"error":"Check your credentials. Some might not reach 3"}), 400

    pwd_hash = bcrypt.generate_password_hash(password).decode("utf-8")

    if User.query.filter_by(username=username).first():
        return jsonify({"message":"Username is taken"})
    elif User.query.filter_by(email=email).first():
        return jsonify({"message":"Email is taken"})
    else:
        user = User(username=username, email=email, password=pwd_hash)
        db.session.add(user)
        db.session.commit()
    
    return jsonify({"message":"User created", 
                    "user":{
                        "username":username, 
                        "email":email, 
                        "password":pwd_hash
                    }    
                }), 201


@users.route("/user/login", methods=["GET","POST"])
def login():
    username = request.json.get("username")
    password = request.json.get("password")

    user = User.query.filter_by(username=username).first()
    hashed_pwd = bcrypt.check_password_hash(user.password, password)

    if user and hashed_pwd:
        refresh_token = create_refresh_token(identity=user.id)
        access_token = create_access_token(identity=user.id)

        return jsonify({
            "message":"Login successful",
            "user":{
                "username":user.username,
                "email":user.email,
                "refresh":refresh_token,
                "access":access_token,
            }
        })
    
    else:
        return jsonify({"error":"Invalid credentials"}), 404


@users.route("/user/refresh", methods=["GET","POST"])
@jwt_required(refresh=True)
def get_access_token_again():
    id_token = get_jwt_identity()
    access = create_access_token(identity=id_token)

    return jsonify({"access":access})


@users.route("/user/profile/<int:id>", methods=["GET","POST"])
@jwt_required()
def user_profile(id):
    current_user = get_jwt_identity()
    profile = User.query.filter_by(id=current_user).first()

    data = []
    for item in profile.bookmark:
        data.append({
            "id":item.id,
            "title":item.title,
            "url":item.url,
            "visits":item.visits,
            "user":item.user_id,
            "created":item.created_at
        })
    
    if len(data) == 0:
        return jsonify({
            "username":profile.username,
            "email":profile.email,
            "bookmarks":"This user has 0 bookmarks"
            }), 200
    
    else:
        return jsonify({
            "message":f"Welcome {profile.username}",
            "number of bookmarks":len(data),
            "bookmarks":data,
        }), 200
    

@users.route("/user/stats", methods=["GET"])
@jwt_required()
def user_stat():
    current_user = get_jwt_identity()
    watch_vids = Bookmark.query.filter_by(user_id=current_user).all()

    data = []
    for item in watch_vids:
        data.append({
            "id":item.id,
            "title":item.title,
            "url":item.url,
            "visits":item.visits,
            "created":item.created_at
        })
    
    if len(data) == 0:
        return jsonify({
            # "message":f"Welcome {watch_vids.user.username}",   //list has no attribute "user"
            "bookmarks":"You have 0 bookmarks"
            }), 200
    
    else:
        return jsonify({
            # "message":f"Welcome {watch_vids.user.username}",   ////list has no attribute "user"
            "number of bookmarks":len(data),
            "bookmarks":data,
        }), 200
