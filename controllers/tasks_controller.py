from models.Task import Task
from datetime import datetime
from main import db
from schemas.TaskSchema import task_schema, tasks_schema
from flask import Blueprint, request, jsonify

tasks = Blueprint('tasks', __name__, url_prefix="/tasks")

@tasks.route("/", methods=["GET"])
def task_index():
    tasks = Task.query.all()
    return jsonify(tasks_schema.dump(tasks))

@tasks.route("/", methods=["POST"])
def task_create():
    task_fields = task_schema.load(request.json)

    # create a new Task object, with the data received in the request
    new_task = Task()
    new_task.name = task_fields["name"]
    new_task.description = task_fields["description"]
    new_task.created = datetime.now()

    #add a new shelter to the db
    db.session.add(new_task)
    db.session.commit()

    return jsonify(task_schema.dump(new_task))