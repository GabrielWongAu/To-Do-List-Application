from models.List import List
from models.Task import Task
from models.User import User
from main import db
from schemas.ListSchema import list_schema, lists_schema
from schemas.TaskSchema import task_schema, tasks_schema
from flask import Blueprint, request, jsonify, render_template, abort, redirect, url_for
# from flask_jwt_extended import jwt_required, get_jwt_identity
# from services.auth_service import verify_user
from flask_login import login_required, current_user

lists = Blueprint('lists', __name__, url_prefix="/lists")

@lists.route("/", methods=["GET"])
def list_index():
    lists = List.query.all()
    #return jsonify(lists_schema.dump(lists))
    return render_template("lists_index.html", lists = lists)

@lists.route("/", methods=["POST"])
@login_required
def list_create():

    name = request.form.get("name")
    description = request.form.get("description")

    list = List.query.filter_by(user_id=current_user.id).first()

    if list:
        return abort(400, description= "Not authorised to create more than one list")

    #list_fields = list_schema.load(request.json)

    # create a new List object, with the data received in the request
    new_list = List()
    new_list.name = name
    new_list.description = description
    new_list.user_id = current_user.id

    #add a new list to the db
    db.session.add(new_list)
    db.session.commit()

    #return jsonify(list_schema.dump(new_list))
    return redirect(url_for('lists.list_index'))

# @lists.route("/", methods=["POST"])
# @jwt_required
# @verify_user
# def list_create():

#     list = List.query.filter_by(user_id=user.id).first()

#     if not list:
#         return abort(400, description= "Not authorized, you need to create a list first")

#     list_fields = list_schema.load(request.json)

#     # create a new List object, with the data received in the request
#     new_list = List()
#     new_list.name = list_fields["name"]
#     new_list.description = list_fields["description"]
#     new_list.user_id = user.id

#     #add a new list to the db
#     db.session.add(new_list)
#     db.session.commit()

#     return jsonify(list_schema.dump(new_list))

@lists.route("/<int:id>", methods=["GET"])
def list_show(id):
    # SELECT * FROM LISTS WHERE ID = id
    list = List.query.get(id)
    #return jsonify(list_schema.dump(list))
    return render_template("list.html", list_individual = list)

@lists.route("/<int:id>/tasks", methods=["GET"])
def list_tasks_show(id):
    # SELECT * FROM TASKS WHERE LIST_ID = id
    tasks = Task.query.filter_by(list_id=id)
    #return jsonify(tasks_schema.dump(tasks))
    return render_template("tasks_index.html", tasks = tasks)

# @lists.route("/<int:id>", methods=["DELETE"])
@lists.route("/delete/<int:id>", methods=["GET"])
@login_required
def list_delete(id):
    # user_id = get_jwt_identity()
    # user = User.query.get(user_id)

    # if not user:
    #     return abort(401, decription="Invalid user")
    
    #list = List.query.get(id)
    list = List.query.filter_by(id=id, user_id=current_user.id).first()
    if not list:
        return abort(400, description="Not authorized to delete other people's lists")
        
    db.session.delete(list)
    db.session.commit()
    #return jsonify(list_schema.dump(list))
    return redirect(url_for('lists.list_index'))

#@jwt_required
@lists.route("/update/<int:id>", methods=["POST"])
@login_required
def list_update(id):
    #make sure the selected list is owned by the logged in user
    list = List.query.filter_by(id=id, user_id=current_user.id).first()
    if not list:
        return abort(400, description="Not authorized to delete other people's list")
    
    #start updating the values of the list according to the form
    list.name = request.form.get("name")
    list.description = request.form.get("description")

    #save the changes
    db.session.commit()
    #return jsonify(list_schema.dump(lists[0]))
    return redirect(url_for('lists.list_index'))

@lists.route("/new", methods=["GET"])
def new_list():
    return render_template("new_list.html")

@lists.route("/modify/<int:id>", methods=["GET"])
def modify_list(id):
    list = list = List.query.get(id)
    return render_template("modify_list.html", list=list)