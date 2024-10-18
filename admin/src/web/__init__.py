from flask import Flask, session
from flask import render_template 
from src.core.models.user import User
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
        user_dict = session.get('user')  # Retrieve the user dictionary from session
        if user_dict:
            user_id = user_dict.get('id')  # Extract the ID from the user dictionary
            if user_id:
                logged_user = User.query.get(user_id)  # Query the User object from the DB
                return {'logged_user': logged_user}
        return {'logged_user': None}

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

    @app.cli.command(name="reset-db")
    def reset_db():
        database.reset()

    @app.cli.command(name="seeds-db")
    def seeds_db():
        seeds.run()

    return app
