from models.Task import Task
from models.List import List
from datetime import datetime
from main import db
from schemas.TaskSchema import task_schema, tasks_schema
from flask import Blueprint, request, jsonify, render_template, abort
from flask_jwt_extended import jwt_required
from services.auth_service import verify_user

tasks = Blueprint('tasks', __name__, url_prefix="/tasks")

@tasks.route("/", methods=["GET"])
def task_index():
    tasks = Task.query.all()
    return jsonify(tasks_schema.dump(tasks))
    #return render_template("tasks_index.html", tasks = tasks)

@tasks.route("/", methods=["POST"])
@jwt_required
@verify_user
def task_create():
    list = List.query.filter_by(user_id=user.id).first()

    if not list:
        return abort(400, description= "Not authorized you need to create a list first")  

    task_fields = task_schema.load(request.json)

    # create a new Task object, with the data received in the request
    new_task = Task()
    new_task.name = task_fields["name"]
    new_task.description = task_fields["description"]
    new_task.created = datetime.now()
    new_task.list_id = list.id

    #add a new task to the db
    db.session.add(new_task)
    db.session.commit()

    return jsonify(task_schema.dump(new_task))

@tasks.route("/<int:id>", methods=["GET"])
def task_show(id):
    # SELECT * FROM TASKS WHERE ID = id
    task = Task.query.get(id)
    # return jsonify(task_schema.dump(task))
    return render_template("task.html", task_individual = task)

@tasks.route("/<int:id>", methods=["DELETE"])
@jwt_required
def task_delete(id):
    task = Task.query.get(id)
    db.session.delete(task)
    db.session.commit()
    return jsonify(task_schema.dump(task))

@tasks.route("/<int:id>", methods=["PUT","PATCH"])
@jwt_required
def task_update(id):
    tasks = Task.query.filter_by(id=id)
    task_fields = task_schema.load(request.json)
    tasks.update(task_fields)
    db.session.commit()
    return jsonify(task_schema.dump(tasks[0]))
