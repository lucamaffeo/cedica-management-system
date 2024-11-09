from marshmallow import Schema
from marshmallow import fields
from src.web.schemas.contactStatus import contact_status_schema

class MessageSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)
    email = fields.Email(required=True)
    body = fields.Str(required=True)
    status = fields.Nested(contact_status_schema, dump_only=True)
    inserted_at = fields.Str(dump_only=True)
    updated_at = fields.Str(dump_only=True)
    #Otros campos: comment

message_schema = MessageSchema()