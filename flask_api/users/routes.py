from flask import Blueprint, request, jsonify
# from flask_api import db, bcrypt
from flask_api.models import User

users = Blueprint("users", __name__)

@users.route("/register", methods=["GET", "POST"])
def register():

    username = request.json.get("username")
    email = request.json.get("email")
    password = request.json.get("password")
    
    if len(username) and len(email) and len(password) < 3:
        return jsonify({"error":"Check your credentials. Some might not reach 3"}), 400

    pwd_hash = bcrypt.generate_password_hash(password)

    user = User(username=username, email=email, password=pwd_hash)
    db.sesion.add(user)
    db.session.commit()

    return jsonify({"message":"User created", 
                    "user":{
                        "username":username, 
                        "email":email, 
                        "password":pwd_hash
                    }    
                })
