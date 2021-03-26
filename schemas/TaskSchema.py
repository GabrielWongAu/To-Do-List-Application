from main import mar
from models.Task import Task

class TaskSchema(mar.SQLAlchemyAutoSchema):
    class Meta:
        model = Task
        include_fk = True

task_schema = TaskSchema()
tasks_schema = TaskSchema(many=True)