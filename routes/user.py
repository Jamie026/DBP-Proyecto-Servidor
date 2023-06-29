from flask import Blueprint, request
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
    return users_data, 200

@users.route("/users/<int:user_id>", methods=["GET"])
def get_user_by_user_id(user_id):
    user = User.query.get(user_id)
    if user is None:
        return {"error": "El usuario no existe"}, 401
    return user.get_data(), 200

@users.route("/@me")
def get_current_user():
    parsed_id = request.cookies.get("code")
    if not parsed_id:
        return {"error": "No autorizado"}, 401
    users = User.query.all()
    user_data = [user for user in users if bcrypt.check_password_hash(parsed_id, str(user.id))]
    if not user_data:
        return {"error": "El usuario no existe"}, 401
    return {"username": user_data[0].username, "id": user_data[0].id}, 200

@users.route("/logout")
def logout():
    return remove_cookie("code"), 200

@users.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    if not validate_data(data, ["username", "password"]):
        return {"error": "Datos incorrectos"}, 403
    username, password = data.get("username"), data.get("password")
    user = User.query.filter_by(username=username).first()
    if user is None:
        return {"error": "Usuario inválido"}, 401
    if not bcrypt.check_password_hash(user.password, password):
        return {"error": "Contraseña inválida"}, 401
    parsed_id = bcrypt.generate_password_hash(str(user.id)).decode("utf-8")
    return set_cookie("code", parsed_id), 200

@users.route("/signup", methods=["POST"])
def signup():
    data = request.get_json()
    if not validate_data(data, ["username", "password", "name", "birthDate", "email"]):
        return {"error": "Datos incorrectos"}, 403
    name, email, birth_date, password, username = data.get("name"), data.get("email"), data.get("birthDate"), data.get("password"), data.get("username")
    existing_user = User.query.filter(or_(User.username == username, User.email == email)).first()
    if existing_user:
        if existing_user.username == username:
            return {"error": "Usuario no disponible"}, 401
        else:
            return {"error": "Email ya registrado"}, 401
    birth_date = datetime.strptime(birth_date, "%Y-%m-%d").date()
    password = bcrypt.generate_password_hash(password).decode("utf-8")
    new_user = User(name, username, password, email, birth_date)
    db.session.add(new_user)
    db.session.commit()
    return set_cookie("code", new_user.id), 200