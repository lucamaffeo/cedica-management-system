from flask import Flask, session
from flask import render_template 
from src.core.models.user import User
from src.core.repositories.riders import has_assignment
from src.core.repositories.user import has_permission
from src.web.handlers import error
from src.web.controllers import register_blueprints
from src.core import database, seeds
from src.core.config import config
import logging
from src.web.storage import storage

logging.basicConfig()
logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)

def create_app(env="development",static_folder="../../static"):
    app = Flask(__name__, static_folder=static_folder)

    app.config.from_object(config[env])
    database.init_app(app)

    # Initialize storage
    storage.init_app(app)

    @app.template_filter('merge')
    def _jinja2_merge(dict1, dict2):
        """Merge two dictionaries."""
        return {**dict1, **dict2}

    @app.context_processor
    def inject_user():
        user_id = session.get('user_id')  # Retrieve the user dictionary from session
        if user_id:
            return {'user_id': user_id}
        return {}

    @app.context_processor
    def inject_has_permission():
        return dict(has_permission=has_permission)

    @app.route("/")
    def home():
        return render_template("home.html")

    @app.route("/about")
    def about():
        return render_template("about.html")

    register_blueprints(app)

    app.register_error_handler(404, error.error_not_found)

    app.register_error_handler(403, error.forbidden)

    app.register_error_handler(401, error.error_unauthorized)

    app.jinja_env.globals.update(has_assignment=has_assignment)

    @app.cli.command(name="reset-db")
    def reset_db():
        database.reset()

    @app.cli.command(name="seeds-db")
    def seeds_db():
        seeds.run()

    return app
