from main import db
from datetime import datetime

class List(db.Model):
    __tablename__="lists"
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(), nullable=False)
    description = db.Column(db.String())
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
