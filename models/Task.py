from main import db
from datetime import datetime

class Task(db.Model):
    __tablename__="tasks"
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(), nullable=False)
    description = db.Column(db.String())
    created = db.Column(db.DateTime, default=datetime.now)
