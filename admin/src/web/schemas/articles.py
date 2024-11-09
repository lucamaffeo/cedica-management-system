from marshmallow import Schema
from marshmallow import fields, validate
from src.web.schemas.user import user_schema

class ArticleSchema(Schema):
    id = fields.Int(dump_only=True)
    title = fields.Str(required=True)
    summary = fields.Str(required=True)
    content = fields.Str(required=True)
    publication_date = fields.DateTime()
    update_date = fields.DateTime(dump_only=True)
    # Autor: autor.name
    author = fields.Nested(user_schema, dump_only=True)
    status = fields.Str(required=True, validate=validate.OneOf(["Borrador", "Publicado", "Archivado"]))

article_schema = ArticleSchema()
articles_schema = ArticleSchema(many=True)

