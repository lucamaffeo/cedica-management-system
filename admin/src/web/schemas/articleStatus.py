from marshmallow import Schema
from marshmallow import fields

class articleStatusSchema(Schema):
    name = fields.Str(required=True)

article_status_schema = articleStatusSchema()