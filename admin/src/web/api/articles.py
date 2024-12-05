from flask import Blueprint
from src.core.repositories import content
from src.core.validation.models.article import ArticleValidator 
from src.web.schemas.articles import articles_schema
from flask import request
from flask import jsonify

bp = Blueprint("articles_api", __name__, url_prefix="/api/articles")


@bp.get("")
def index():
    # Validar todos los campos, en caso de que estén mal devolver error.
    params = request.args.to_dict()

    validator = ArticleValidator()
    errors = validator.validate_request(params)

    if errors:
        return jsonify({"errors": errors}), 400
    
    author = request.args.get('author')
    published_from = request.args.get('published_from')
    published_to = request.args.get('published_to')
    # Si no se envía el parámetro, se asigna el valor por defecto. Si se envía con valor '', también se asigna el valor por defecto.
    page = int(request.args.get('page', '1') or '1')
    per_page = int(request.args.get('per_page', '10') or '10')

    articles = content.list_contents_api(
        author=author, published_from=published_from, published_to=published_to, page=page, per_page=per_page)
    data = articles_schema.dump(articles.items)

    return jsonify({"data": data, "page": page, "per_page": per_page, "total": articles.total}), 200
