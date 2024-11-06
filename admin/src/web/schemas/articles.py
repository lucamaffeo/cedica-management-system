from marshmallow import Schema
from marshmallow import fields

class ArticleSchema(Schema):
    id = fields.int()
    title = fields.Str()