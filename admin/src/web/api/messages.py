from flask import Blueprint, request, jsonify
import requests
from src.core.repositories import contact
from src.web.schemas.messages import message_schema

bp = Blueprint("messages_api", __name__, url_prefix="/api/messages")

def validate_captcha(captcha_response):
    secret_key = "6Lf0IoEqAAAAAOjZMQVfQVU5vYjaDXKRviS1QAoY"
    verify_url = "https://www.google.com/recaptcha/api/siteverify"
    payload = {"secret": secret_key, "response": captcha_response}
    
    try:
        response = requests.post(verify_url, data=payload)
        result = response.json()
    except requests.exceptions.RequestException as e:
        return False

    return result.get("success", False)

@bp.route("", methods=["GET", "POST"])
def handle_messages():
    if request.method == "POST":
        attributes = request.get_json()

        # Validar datos del formulario
        errors = message_schema.validate(attributes)
        if errors:
            return jsonify({"errors": errors}), 400

        # Validar el token de reCAPTCHA
        if not validate_captcha(attributes.get("captcha")):
            return jsonify({"errors": {"captcha": ["Captcha inválido"]}}), 400
        
        attributes.pop("captcha", None)  # Elimina el campo 'captcha' si existe

        # Crear el mensaje en la base de datos
        kwargs = message_schema.load(attributes)
        new_message = contact.create_contact(**kwargs)
        data = message_schema.dump(new_message)
        return jsonify(data), 201

    elif request.method == "GET":
        # Obtener todos los mensajes
        messages = contact.list_contacts()
        return jsonify([message.to_dict() for message in messages]), 200
