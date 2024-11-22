from marshmallow import Schema
from marshmallow import fields, validate
from src.web.schemas.contactStatus import contact_status_schema


class MessageSchema(Schema):
    title = fields.Str(required=True, validate=validate.Length(min=2, max=255))
    email = fields.Email(
        required=True, validate=validate.Length(min=2, max=255))
    description = fields.Str(
        required=True, validate=validate.Length(min=2, max=255))
    status = fields.Nested(contact_status_schema, dump_only=True)
    inserted_at = fields.Str(dump_only=True)
    updated_at = fields.Str(dump_only=True)
    # Otros campos: comment


message_schema = MessageSchema()
