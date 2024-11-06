from flask import Blueprint

bp = Blueprint("messages_api", __name__, url_prefix="/api/messages")

@bp.get("/")
def index():

    return {"status": "succes"}, 200