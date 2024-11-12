from marshmallow import Schema
from marshmallow import fields

class UserSchema(Schema):
    alias = fields.Str(required=True)

user_schema = UserSchema()