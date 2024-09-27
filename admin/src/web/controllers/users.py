from flask import Blueprint
from flask import render_template

from src.core import auth
from src.web.helpers.auth import login_required

user_blueprint = Blueprint("users", __name__, url_prefix="/users")


@user_blueprint.route("/")
@login_required
def index():
    users = auth.list_users()
    return render_template("users/index.html", users=users)

@user_blueprint.route("/create", methods=["POST"])
@login_required
def create():
    if request.method == "POST":
        params = request.form
        auth.create_user(
            email=params["email"],
            password=params["password"],
            role_id=params["role_id"],
            alias=params["alias"],
        )
        return redirect(url_for("users.index"))
    return render_template("users/create.html")
