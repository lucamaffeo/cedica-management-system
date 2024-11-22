from flask import Blueprint, request, jsonify
import requests
from src.core.repositories import contact
from src.web.schemas.messages import message_schema

bp = Blueprint("messages_api", __name__, url_prefix="/api/messages")


@bp.route("", methods=["POST"])
def handle_messages():

    attributes = request.get_json()

    # Validar datos del formulario
    errors = message_schema.validate(attributes)
    if errors:
        return jsonify({"errors": errors}), 400
    # Crear el mensaje en la base de datos
    kwargs = message_schema.load(attributes)
    new_message = contact.create_contact(**kwargs)
    data = message_schema.dump(new_message)
    return jsonify(data), 201

