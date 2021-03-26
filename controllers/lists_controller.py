from models.List import List
from main import db
from schemas.ListSchema import list_schema, lists_schema
from flask import Blueprint, request, jsonify

lists = Blueprint('lists', __name__, url_prefix="/lists")

@lists.route("/", methods=["GET"])
def list_index():
    lists = List.query.all()
    return jsonify(lists_schema.dump(lists))

@lists.route("/", methods=["POST"])
def list_create():
    list_fields = list_schema.load(request.json)

    # create a new List object, with the data received in the request
    new_list = List()
    new_list.name = list_fields["name"]
    new_list.description = list_fields["description"]

    #add a new list to the db
    db.session.add(new_list)
    db.session.commit()

    return jsonify(list_schema.dump(new_list))

@lists.route("/<int:id>", methods=["GET"])
def list_show(id):
    # SELECT * FROM LISTS WHERE ID = id
    list = List.query.get(id)
    return jsonify(list_schema.dump(list))

@lists.route("/<int:id>", methods=["DELETE"])
def list_delete(id):
    list = List.query.get(id)
    db.session.delete(list)
    db.session.commit()
    return jsonify(list_schema.dump(list))

@lists.route("/<int:id>", methods=["PUT","PATCH"])
def list_update(id):
    lists = List.query.filter_by(id=id)
    list_fields = list_schema.load(request.json)
    lists.update(list_fields)
    db.session.commit()
    return jsonify(list_schema.dump(lists[0]))