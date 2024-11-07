from flask import Blueprint
from src.core.repositories import content
from src.web.schemas.articles import articles_schema, article_schema
from flask import request
from flask import jsonify

bp = Blueprint("articles_api", __name__, url_prefix="/api/articles")

@bp.get("/")
def index():
    #Agregar validadores de fecha
    author = request.args.get('author')
    published_from = request.args.get('published_from')
    published_to = request.args.get('published_to')
    page = int(request.args.get('page', 1))
    per_page = int(request.args.get('per_page', 10))


    articles = content.list_contents_api(author=author, published_from=published_from, published_to=published_to, page=page, per_page=per_page)
    total = content.total_contents()
    data = articles_schema.dump(articles.items)
    
    return {"data": data, "page": page, "per_page":per_page, "total": total}, 200

@bp.post("/")
def create():
    atributes = request.get_json()
    errors = article_schema.validate(atributes)
    if errors:
        return {"errors": errors}, 400
    else:
        kwars = article_schema.load(atributes)
        # Pueden ocurrir errores al insertar en la base de datos!
        new_article = content.create_content(**kwars)
        data = article_schema.dump(new_article)
        return jsonify(atributes), 201