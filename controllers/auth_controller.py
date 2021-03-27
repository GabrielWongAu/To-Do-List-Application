from models.User import User
from schemas.UserSchema import user_schema
from main import db
from flask import Blueprint, request, jsonify, abort

auth = Blueprint('auth', __name__, url_prefix="/auth")

@auth.route("/signup", methods=["POST"])
def auth_register():
    user_fields = user_schema.load(request.json)

    #avoid creating a user that already exists
    user = User.query.filter_by(username=user_fields["username"]).first()

    if user:
        return abort(400, description="User already exists")
    
    user = User()
    user.username = user_fields["username"]
    user.password = user_fields["password"]

    db.session.add(user)
    db.session.commit()

    return jsonify(user_schema.dump(user))