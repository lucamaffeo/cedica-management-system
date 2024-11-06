from flask import Blueprint

bp = Blueprint("articles_api", __name__, url_prefix="/api/articles")

@bp.get("/")
def index():

    return {"status": "succes"}, 200