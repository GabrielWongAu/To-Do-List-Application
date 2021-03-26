from main import mar
from models.List import List

class ListSchema(mar.SQLAlchemyAutoSchema):
    class Meta:
        model = List

list_schema = ListSchema()
lists_schema = ListSchema(many=True)