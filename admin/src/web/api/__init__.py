from .articles import bp as articles_api
from .messages import bp as messages_api


def register_api_blueprints(app):
    """Register all api blueprints with the Flask app."""
    app.register_blueprint(articles_api)
    app.register_blueprint(messages_api)
