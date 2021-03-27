from main import mar
from models.Task import Task
from schemas.ListSchema import ListSchema

class TaskSchema(mar.SQLAlchemyAutoSchema):
    class Meta:
        model = Task
        #include_fk = True
    list = mar.Nested(ListSchema)

task_schema = TaskSchema()
tasks_schema = TaskSchema(many=True)