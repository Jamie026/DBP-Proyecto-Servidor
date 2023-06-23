from flask import Blueprint, jsonify, request
from models.group import Group
from models.rol import Rol
from models.db import db
from datetime import datetime

groups = Blueprint("groups", __name__)

@groups.route("/groups", methods=["GET"])
def getGroups():
    groups = Group.query.all()
    groupsJson = [group.to_dict() for group in groups]
    return jsonify(groupsJson), 200

@groups.route("/groups/<int:userID>", methods=["GET"])
def getGroupsByUserId(userID):
    rols = Rol.query.filter_by(user=userID).all()
    groupsJson, members, admins = ([], [], [])
    for rol in rols:
        group = Group.query.get(rol.group)
        groupsJson.append(group.to_dict())
        admins.append(rol.admin)
        members.append(Rol.query.filter_by(group=group.id).count())
    return jsonify({"groups": groupsJson, "members": members, "admins": admins}), 200

@groups.route("/createGroup", methods=["POST"])
def create_group():
    data = request.get_json()
    name, password, date, user =  data.get("name"), data.get("password"), data.get("date"), data.get("user")
    date = datetime.strptime(date, "%Y-%m-%d")
    newGroup = Group(name, password, date)
    db.session.add(newGroup)
    db.session.commit()
    createMember(user, newGroup.id, True)
    return jsonify({"message": "Grupo creado", "id": newGroup.id}), 200

@groups.route("/joinGroup", methods=["POST"])
def joinGroup():
    data = request.get_json()
    id, password, user = data.get("id"), data.get("password"), data.get("user")
    group = Group.query.get(id)
    if not group:
        return jsonify({"error": "El grupo no existe"}), 401
    if not group.password == password:
        return jsonify({"error": "Contraseña incorrecta"}), 401
    response = createMember(user, id, False)
    if response:
        members = Rol.query.filter_by(group=id).count()
        return jsonify({"message": "Unido al grupo", "id": id, "name": group.name, "members": members}), 200
    return jsonify({"error": "Ya pertenece al grupo"}), 403 

@groups.route("/deleteMember", methods=["POST"])
def deleteMember():
    data = request.get_json()
    user, group = data.get("user"), data.get("group")
    members = Rol.query.filter_by(group=group).all()
    if len(members) == 1:
        db.session.delete(members[0])
        db.session.delete(Group.query.get(group))
        db.session.commit()
    else:
        admins = Rol.query.filter_by(group=group, admin=True).all()
        if len(admins) == 1 and admins[0].user == user:
            return jsonify({"error": "Usted es el unico administrador del grupo"}), 403 
        else:
            db.session.delete(admins[0])
    return jsonify({"message": "Salida del grupo exitosa"}), 200
    
def createMember(user, group, admin):
    rolExist = Rol.query.filter_by(user=user, group=group).first() is not None
    if rolExist:
        return False
    newRol = Rol(user, group, admin)
    db.session.add(newRol)
    db.session.commit()
    return True