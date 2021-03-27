from main import mar
from models.List import List
from schemas.UserSchema import UserSchema

class ListSchema(mar.SQLAlchemyAutoSchema):
    class Meta:
        model = List
    user = mar.Nested(UserSchema)

list_schema = ListSchema()
lists_schema = ListSchema(many=True)