from models.Task import Task
from main import db
from schemas.TaskSchema import task_schema, tasks_schema
from flask import Blueprint, request, jsonify

tasks = Blueprint('tasks', __name__, url_prefix="/tasks")

@tasks.route("/", methods=["GET"])
def task_index():
    tasks = Task.query.all()
    return jsonify(tasks_schema.dump(tasks))
    