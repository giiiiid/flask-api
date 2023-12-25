from flask import Blueprint, request, jsonify, json
from flask_api.utils import bcrypt, db
from flask_api.models import User
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
            "message":"Login successfully",
            "user":{
                "refresh":refresh_token,
                "access":access_token,
                "username":username
            }
        })
    
    else:
        return jsonify({"error":"Invalid credentials"}), 400


@users.route("/try", methods=["GET","POST"])
@jwt_required()
def try_jwt():
    user_id = get_jwt_identity()

    user = User.query.filter_by(id=user_id).first()
    
    if not user:
        return jsonify({"error":"Invalid user"}), 400
    
    return jsonify({
        "message":"me tried",
        "username":user.username,
        "email":user.email,
    }), 200


@users.route("/user/refresh-token", methods=["GET"])
@jwt_required(refresh=True)
def refresh_access_token():
    id = get_jwt_identity()
    access = create_access_token(identity=id)

    return jsonify({"access":access}), 200