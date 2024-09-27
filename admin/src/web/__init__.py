from flask import Flask, redirect, request, session, url_for
from flask import render_template 
from src.web.handlers import error
from src.web.controllers.auth import bp as auth_bp
from src.core import database, seeds
from src.core.config import config

def create_app(env="development",static_folder="../../static"):
    app = Flask(__name__, static_folder=static_folder)   

    app.config.from_object(config[env])
    database.init_app(app)

    @app.context_processor
    def inject_user():
        return {'user': session.get('user')}

    @app.route("/")
    def home():
        return render_template("home.html")
    
    app.register_blueprint(auth_bp)

    @app.route("/about")
    def about():
        return render_template("about.html")

    @app.route("/login", methods=['GET', 'POST'])
    def login():
        if request.method == 'POST':
            ## login logic
            email = request.form.get('email')
            password = request.form.get('password')
            return redirect(url_for('home'))
        return render_template('auth/login.html')

    app.register_error_handler(404, error.error_not_found)

    @app.cli.command(name="reset-db")
    def reset_db():
        database.reset()

    @app.cli.command(name="seeds-db")
    def seeds_db():
        seeds.run()
        
    return app
