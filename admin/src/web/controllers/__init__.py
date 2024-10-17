from .auth import bp as auth
from .users import bp as users
from .payments import bp as payments
from .employees import bp as employees
from .horses import bp as horses
from .receipt import bp as receipt

def register_blueprints(app):
    """Register all blueprints with the Flask app."""
    app.register_blueprint(auth)
    app.register_blueprint(users)
    app.register_blueprint(payments)
    app.register_blueprint(employees)
    app.register_blueprint(horses)
    app.register_blueprint(receipt)
