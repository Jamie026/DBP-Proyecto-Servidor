from datetime import datetime
from flask import Blueprint, jsonify, request
from models.task import Task
from models.assign import Assign
from models.rol import Rol
from models.db import db

tasks = Blueprint("tasks", __name__)

@tasks.route("/tasks/<int:userID>", methods=["GET"])
def getTasksByUserId(userID):
    tasks = Task.query.filter_by(user=userID, active=True).all()
    assigns, tasksJson = ([], [])
    for task in tasks:
        assigns.append(Assign.query.filter_by(task=task.id).count())    
        tasksJson.append(task.to_dict())    
    return jsonify({"tasks": tasksJson, "assigns": assigns}), 200

@tasks.route("/createTask", methods=["POST"])
def createTask():
    data = request.get_json()
    name, description, date, user =  data.get("name"), data.get("description"), data.get("date"), data.get("user")
    date = datetime.strptime(date, "%Y-%m-%d")
    newTask = Task(name, description, date, user)
    db.session.add(newTask)
    db.session.commit()
    return jsonify({"message": "Tarea creada", "id": newTask.id}), 200

@tasks.route("/assignTask", methods=["POST"])
def assignTask():
    data = request.get_json()
    group, task, user = data.get("group"), data.get("task"), data.get("user")
    taskExist = Task.query.filter_by(id=task, user=user).first()
    if taskExist is None:
        return jsonify({"error": "Tarea no disponible"}), 401
    rol = Rol.query.filter_by(group=group, user=user).first()
    if rol is None:
        return jsonify({"error": "Usted no pertenece al grupo"}), 401
    if rol.admin is False:
        return jsonify({"error": "No tiene autorización"}), 401
    assignExist = Assign.query.filter_by(group=group, task=task).first() is not None
    if assignExist:
        return jsonify({"error": "Tarea ya asignada al grupo"}), 401
    newAssign = Assign(task, group)
    db.session.add(newAssign)
    db.session.commit()
    return jsonify({"message": "Tarea asignada"}), 200

@tasks.route("/deleteTask/<int:taskID>", methods=["DELETE"])
def deleteTask(taskID):
    task = Task.query.filter_by(id=taskID).first()
    if task is None:
        return jsonify({"error": "Tarea no disponible"}), 401
    task.active = False
    db.session.commit()
    return jsonify({"message": "Tarea eliminada"}), 200