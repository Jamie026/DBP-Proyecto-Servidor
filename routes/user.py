from flask import Blueprint, request, jsonify
from datetime import datetime
from flask_bcrypt import Bcrypt
from models.user import User
from models.db import db
from sqlalchemy import or_
from utils.functions import set_cookie, remove_cookie, validate_data

users = Blueprint("users", __name__)
bcrypt = Bcrypt()

@users.route("/users", methods=["GET"])
def get_users():
    users = User.query.all()
    users_data = [user.get_data() for user in users]
    return jsonify(result={"users": users_data}), 200

@users.route("/users/<int:user_id>", methods=["GET"])
def get_user_by_user_id(user_id):
    user = User.query.get(user_id)
    if user is None:
        return jsonify(result={"error": "El usuario no existe"}), 401
    return jsonify(result={"user": user.get_data()}), 200

@users.route("/@me")
def get_current_user():
    parsed_id = request.cookies.get("code")
    print(parsed_id)
    if not parsed_id:
        return {"error": "No autorizado"}, 401
    users = User.query.all()
    user_match = [user for user in users if bcrypt.check_password_hash(parsed_id, str(user.id))]
    if len(user_match) == 0:
        return jsonify(result={"error": "El usuario no existe"}), 401
    return jsonify(result={"user": user_match[0].get_data()}), 200

@users.route("/logout")
def logout():
    return remove_cookie("code"), 200

@users.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    if not validate_data(data, ["username", "password"]):
        return jsonify(result={"error": "Datos incorrectos"}), 403
    username, password = data.get("username"), data.get("password")
    user = User.query.filter_by(username=username).first()
    if user is None:
        return jsonify(result={"error": "Usuario inválido"}), 401
    if not bcrypt.check_password_hash(user.password, password):
        return jsonify(result={"error": "Contraseña inválida"}), 401
    parsed_id = bcrypt.generate_password_hash(str(user.id)).decode("utf-8")
    return set_cookie("code", parsed_id), 200

@users.route("/signup", methods=["POST"])
def signup():
    data = request.get_json()
    if not validate_data(data, ["username", "password", "name", "birthDate", "email"]):
        return jsonify(result={"error": "Datos incorrectos"}), 403
    name, email, birth_date, password, username = data.get("name"), data.get("email"), data.get("birthDate"), data.get("password"), data.get("username")
    existing_user = User.query.filter(or_(User.username == username, User.email == email)).first()
    if existing_user:
        if existing_user.username == username:
            return jsonify(result={"error": "Usuario no disponible"}), 401
        else:
            return jsonify(result={"error": "Email ya registrado"}), 401
    birth_date = datetime.strptime(birth_date, "%Y-%m-%d").date()
    password = bcrypt.generate_password_hash(password).decode("utf-8")
    new_user = User(name, username, password, email, birth_date)
    db.session.add(new_user)
    db.session.commit()
    parsed_id = bcrypt.generate_password_hash(str(new_user.id)).decode("utf-8")
    return set_cookie("code", parsed_id), 200
