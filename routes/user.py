from datetime import datetime
from flask import Blueprint, jsonify, request, make_response
from models.user import User
from flask_bcrypt import Bcrypt
from models.db import db

users = Blueprint("users", __name__)
bcrypt = Bcrypt()

@users.route("/users", methods=["GET"])
def getUsers():
    users = User.query.all()
    usersJson = [user.to_dict() for user in users]
    return jsonify(usersJson), 200

@users.route("/users/<int:id>", methods=["GET"])
def getUserByUserId(id):
    user = User.query.get(id)
    if not user:
        return jsonify({"error": "El usuario no existe"}), 401
    return jsonify(user.to_dict()), 200

@users.route("/@me")
def get_current_user():
    userID = request.cookies.get("userID")
    if not userID:
        return jsonify({"error": "No autorizado"}), 401
    user = User.query.get(userID)
    return jsonify({"user": user.user, "id": user.id}), 200

@users.route("/logout")
def logout():
    userID = request.cookies.get("userID")
    if not userID:
        return jsonify({"error": "No autorizado"}), 401
    return removeCookie("userID"), 200

@users.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    user, password = data.get("user"), data.get("password")
    user = User.query.filter_by(user=user).first()
    if user is None:
        return jsonify({"error": "Usuario inválido"}), 401
    if not bcrypt.check_password_hash(user.password, password):
        return jsonify({"error": "Contraseña inválida"}), 401
    return setCookie("userID", user.id), 200

@users.route("/signup", methods=["POST"])
def signup():
    data = request.get_json()
    name, email, birthDate, password, user = data.get("name"), data.get("email"), data.get("birthDate"), data.get("password"), data.get("user")
    userExist = User.query.filter_by(user=user).first() is not None
    if userExist:
        return jsonify({"error": "Usuario no disponible"}), 401
    birthDate = datetime.strptime(birthDate, "%Y-%m-%d").date()
    password = bcrypt.generate_password_hash(password).decode("utf-8")
    newUser = User(name, user, password, email, birthDate)
    db.session.add(newUser)
    db.session.commit()
    return setCookie("userID", newUser.id), 200

def setCookie(key, value):
    response = make_response("Cookie establecida")
    response.set_cookie(key, str(value), secure=True, samesite="None")
    return response

def removeCookie(key):
    response = make_response("Cookie eliminada")
    response.set_cookie(key, "", secure=True, samesite="None", expires=0)
    return response