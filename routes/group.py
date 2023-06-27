from flask import Blueprint, request
from utils.functions import validate_data
from datetime import datetime
from models.group import Group
from models.rol import Rol
from models.user import User
from models.db import db

groups = Blueprint("groups", __name__)

@groups.route("/groups", methods=["GET"])
def get_groups():
    groups = Group.query.all()
    groups_data = [group.get_data() for group in groups]
    return groups_data, 200

@groups.route("/groups/<int:user_id>", methods=["GET"])
def get_groups_by_user_id(user_id):
    roles = Rol.query.filter_by(user=user_id).all()
    groups, members, admins = [], [], []
    for rol in roles:
        group = Group.query.get(rol.group)
        groups.append(group.get_data())
        admins.append(rol.admin)
        members.append(Rol.query.filter_by(group=group.id).count())
    return {"groups": groups, "members": members, "admins": admins}, 200

@groups.route("/checkMember/<int:group_id>/<int:user_id>", methods=["GET"])
def check_member(group_id, user_id):
    admin = Rol.query.filter_by(user=user_id, group=group_id, admin=True).first()
    if not admin:
        return {"error": "No tienes permisos de administrador"}, 403
    return {"message": "Tienes permisos de administrador"}, 200

@groups.route("/members/<int:group_id>", methods=["GET"])
def get_members(group_id):
    roles = Rol.query.filter_by(group=group_id).all()
    members, admins = [], []
    for rol in roles:
        user = User.query.get(rol.user)
        admins.append(rol.admin)
        members.append(user.get_data())
    return {"members": members, "admins": admins}, 200

@groups.route("/createGroup", methods=["POST"])
def create_group():
    data = request.get_json()
    if not validate_data(data, ["name", "password", "date", "user"]):
        return {"error": "Datos incorrectos"}, 403
    name, password, date, user_id = data.get("name"), data.get("password"), data.get("date"), data.get("user")
    date = datetime.strptime(date, "%Y-%m-%d").date()
    new_group = Group(name, password, date)
    db.session.add(new_group)
    db.session.commit()
    create_member(user_id, new_group.id, True)
    return {"message": "Grupo creado", "id": new_group.id}, 200

@groups.route("/joinGroup", methods=["POST"])
def join_group():
    data = request.get_json()
    if not validate_data(data, ["group", "password", "user"]):
        return {"error": "Datos incorrectos"}, 403
    group_id, password, user_id = data.get("group"), data.get("password"), data.get("user")
    group = Group.query.get(group_id)
    user = User.query.get(user_id)
    if not group:
        return {"error": "El grupo no existe"}, 401
    if not group.password == password:
        return {"error": "Contraseña incorrecta"}, 401
    new_member = create_member(user_id, group_id, False)
    if new_member:
        members = Rol.query.filter_by(group=group_id).count()
        return {"message": "Unido al grupo", "id": group.id, "name": group.name, "members": members}, 200
    return {"error": "Ya pertenece al grupo"}, 403

@groups.route("/deleteMember/<int:group_id>/<int:user_id>", methods=["DELETE"])
def delete_member(group_id, user_id):
    members = Rol.query.filter_by(group=group_id).all()
    if len(members) == 1:
        db.session.delete(Group.query.get(group_id))
    else:
        admins = [member for member in members if member.admin]        
        if len(admins) == 1 and admins[0].user == user_id:
            return {"error": "Usted es el único administrador del grupo"}, 403
        db.session.delete(Rol.query.filter_by(group=group_id, user=user_id))
    db.session.commit()
    return {"message": "Salida del grupo exitosa"}, 200

def create_member(user_id, group_id, admin):
    member = Rol.query.filter_by(user=user_id, group=group_id).first()
    if member is not None:
        return False
    new_rol = Rol(user_id, group_id, admin)
    db.session.add(new_rol)
    db.session.commit()
    return True