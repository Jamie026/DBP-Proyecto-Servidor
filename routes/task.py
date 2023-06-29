from flask import Blueprint, request
from datetime import datetime
from utils.functions import validate_data
from models.user import User
from models.task import Task
from models.group import Group
from models.assign import Assign
from models.rol import Rol
from models.db import db

tasks = Blueprint("tasks", __name__)

@tasks.route("/tasks/<int:user_id>", methods=["GET"])
def get_tasks_by_user_id(user_id):
    tasks = Task.query.filter_by(user=user_id).all()
    assigns, tasks_data = [], []
    for task in tasks:
        assigns.append(Assign.query.filter_by(task=task.id).count())    
        tasks_data.append(task.get_data())    
    return {"tasks": tasks_data, "assigns": assigns}, 200

@tasks.route("/createTask", methods=["POST"])
def create_task():
    data = request.get_json()
    if not validate_data(data, ["name", "description", "date", "user"]):
        return {"error": "Datos incorrectos"}, 403
    name, description, date, user_id =  data.get("name"), data.get("description"), data.get("date"), data.get("user")
    date = datetime.strptime(date, "%Y-%m-%d")
    user = User.query.get(user_id)
    if user is None:
        return {"error": "Usuario no encontrado"}, 401
    new_task = Task(name, description, date, user_id)
    db.session.add(new_task)
    db.session.commit()
    return {"message": "Tarea creada", "id": new_task.id}, 200

@tasks.route("/assignTask", methods=["POST"])
def assign_task():
    data = request.get_json()
    if not validate_data(data, ["task", "user", "group"]):
        return {"error": "Datos incorrectos"}, 403
    group_id, task_id, user_id = data.get("group"), data.get("task"), data.get("user")
    group = Group.query.get(group_id)
    task = Task.query.get(task_id)
    rol = Rol.query.filter_by(group=group_id, user=user_id).first()
    if group is None:
        return {"error": "Grupo no encontrado"}, 401
    if task is None:
        return {"error": "Tarea no disponible"}, 401
    if rol is None:
        return {"error": "Usted no pertenece al grupo"}, 401
    if not rol.admin:
        return {"error": "No tiene autorización"}, 401
    assign = Assign.query.filter_by(group=group_id, task=task_id).first() 
    if assign is not None:
        return {"error": "Tarea ya asignada al grupo"}, 401
    new_assign = Assign(task_id, group_id)
    db.session.add(new_assign)
    db.session.commit()
    return {"message": "Tarea asignada"}, 200

@tasks.route("/deleteTask/<int:task_id>", methods=["DELETE"])
def delete_task(task_id):
    task = Task.query.get(task_id)
    if task is None:
        return {"error": "Tarea no disponible"}, 401
    assigns = Assign.query.filter_by(task=task.id).count()
    if assigns > 0:
        return {"error": "La tarea tiene asignaciones"}, 401
    db.session.delete(task)
    db.session.commit()
    return {"message": "Tarea eliminada"}, 200