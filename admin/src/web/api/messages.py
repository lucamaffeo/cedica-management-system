from flask import Blueprint
from src.core.repositories import contact
from src.web.schemas.messages import message_schema
from flask import request
from flask import jsonify

bp = Blueprint("messages_api", __name__, url_prefix="/api/messages")

@bp.post("/")
def create():
    atributes = request.get_json()
    errors = message_schema.validate(atributes)
    if errors:
        return {"errors": errors}, 400
    else:
        kwars = message_schema.load(atributes)
        # Pueden ocurrir errores al insertar en la base de datos!
        new_message = contact.create_contact(**kwars)
        data = message_schema.dump(new_message)
        return jsonify(data), 201