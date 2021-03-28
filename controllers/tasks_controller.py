from models.Task import Task
from models.List import List
from models.User import User
from datetime import datetime
from main import db
from schemas.TaskSchema import task_schema, tasks_schema
from schemas.ListSchema import list_schema, lists_schema
from flask import Blueprint, request, jsonify, render_template, abort, redirect, url_for
from flask_login import login_required, current_user
# from flask_jwt_extended import jwt_required
# from services.auth_service import verify_user


tasks = Blueprint('tasks', __name__, url_prefix="/tasks")

@tasks.route("/", methods=["GET"])
def task_index():
    tasks = Task.query.all()
    #return jsonify(tasks_schema.dump(tasks))
    return render_template("tasks_index.html", tasks_render=tasks)

@tasks.route("/", methods=["POST"])
@login_required
def task_create():
    list = List.query.filter_by(user_id=user.id).first()

    if not list:
        return abort(400, description= "Not authorized you need to create a list first")  

    #task_fields = task_schema.load(request.json)

    # create a new Task object, with the data received in the request
    new_task = Task()
    new_task.name = request.form.get("name")
    new_task.description = request.form.get("description")
    new_task.created = datetime.now()
    new_task.list_id = list.id

    #add a new task to the db
    db.session.add(new_task)
    db.session.commit()

    #return jsonify(task_schema.dump(new_task))
    return redirect(url_for('task.task_index'))

@tasks.route("/<int:id>", methods=["GET"])
def task_show(id):
    # SELECT * FROM TASKS WHERE ID = id
    task = Task.query.get(id)
    # return jsonify(task_schema.dump(task))
    return render_template("task.html", task=task)

@tasks.route("/delete/<int:id>", methods=["DELETE"])
@login_required
def task_delete(id):
    task = Task.query.get(id)

    list = List.query.filter_by(id=task.list_id, user_id=current_user.id).first()

    if not list:
        return abort(400, description= "Not authorised, this task does not belong to your list")
    
    db.session.delete(task)
    db.session.commit()
    #return jsonify(task_schema.dump(task))
    return redirect(url_for('tasks.task_index'))


@tasks.route("/update/<int:id>", methods=["POST"])
@login_required
def task_update(id):
    task = Task.query.get(id)
    list = List.query.filter_by(id=task.list_id, user_id=current_user.id).first()

    if not list:
        return abort(400, description= "Not authorised, this task does not belong to your list")
    
    #start updating the values of the task according to the form
    task.name = request.form.get("name")
    task.description = request.form.get("description")
    list.user_id = current_user.id

    #save the changes
    db.session.commit()
    #return jsonify(task_schema.dump(tasks[0]))
    return redirect(url_for('tasks.task_index'))

@tasks.route("/new", methods=["GET"])
def new_taskask():
    return render_template("new_task.html")

@tasks.route("/modify/<int:id>", methods=["GET"])
def modify_task(id):
    task = Task.query.get(id)
    return render_template("modify_task.html", task=task)