from flask import Blueprint, request, jsonify
from flaskapi import db, bcrypt, login_user
from flaskapi.models import User

users = Blueprint("users", __name__)

@users.route("/register", methods=["GET", "POST"])
def register():
    return "Hello"
    # username = request.json["username"]
    # email = request.json["email"]
    # password = request.json["password"]
    
    # if len(username) and len(email) and len(password) < 3:
    #     return jsonify({"error":"Check your credentials. Some might not reach 3"}), 400

    # pwd_hash = bcrypt.generate_password_hash(password)

    # user = User(username=username, email=email, password=pwd_hash)
    # db.sesion.add(user)
    # db.session.commit()

    # return jsonify({"message":"User created", 
    #                 "user":{
    #                     "username":username, 
    #                     "email":email, 
    #                     "password":pwd_hash
    #                 }    
    #             })
