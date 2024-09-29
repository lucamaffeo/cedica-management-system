from flask import Flask, session
from flask import render_template 
from src.web.handlers import error
from src.web.controllers import register_blueprints
from src.core import database, seeds
from src.core.config import config

def create_app(env="development",static_folder="../../static"):
    app = Flask(__name__, static_folder=static_folder)   

    app.config.from_object(config[env])
    database.init_app(app)

    @app.template_filter('merge')
    def merge(dict1, dict2):
        """Merge two dictionaries."""
        return {**dict1, **dict2}

    @app.context_processor
    def inject_user():
        return {'logged_user': session.get('user')}

    @app.route("/")
    def home():
        return render_template("home.html")

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
