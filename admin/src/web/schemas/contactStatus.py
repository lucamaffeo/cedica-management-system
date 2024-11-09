from marshmallow import Schema
from marshmallow import fields

class contacStatusSchema(Schema):
    name = fields.Str(required=True)

contact_status_schema = contacStatusSchema()