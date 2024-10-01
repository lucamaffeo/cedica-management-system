from .auth import bp as auth_bp
from .users import bp as users_bp

def register_blueprints(app):
    """Register all blueprints with the Flask app."""
    app.register_blueprint(auth_bp)
    app.register_blueprint(users_bp)
