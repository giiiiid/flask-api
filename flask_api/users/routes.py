from flask import Blueprint, request, jsonify, json
from flask_api.utils import bcrypt
from flask_api.models import User, db


users = Blueprint("users", __name__)

@users.route("/register", methods=["GET", "POST"])
def register():

    username = request.json.get("username")
    email = request.json.get("email")
    password = request.json.get("password")
    
    if len(username) and len(email) and len(password) < 3:
        return jsonify({"error":"Check your credentials. Some might not reach 3"}), 400

    pwd_hash = bcrypt.generate_password_hash(password).decode("utf-8")

    user = User(username=username, email=email, password=pwd_hash)
    db.session.add(user)
    db.session.commit()
    
    users = User.query.all()
    print(users)
    
    return jsonify({"message":"User created", 
                    "user":{
                        "username":username, 
                        "email":email, 
                        "password":pwd_hash
                    }    
                })

