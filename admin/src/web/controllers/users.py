from flask import Blueprint, redirect, render_template, request, url_for

from src.core import auth
from src.web.helpers.auth import has_permissions, login_required

bp = Blueprint("users", __name__, url_prefix="/users")

# register
@bp.get("/register")
def register():
    return render_template("users/form.html", is_update=False, title='Crear Usuario')

@bp.get("/<int:id>/update")
def edit(id):
    user = auth.get_user(id)
    return render_template("users/form.html", is_update=True, title='Actualizar Usuario', user=user)

@bp.post("/<int:id>/update")
def update(id):
    if request.method == "POST":
        params = request.form
        _ = auth.update_user(
            id=id,
            alias=params["alias"],
            email=params["email"],
            active= 'active' in params,
            role_id=params["role_id"],
        )
        return redirect(url_for("users.index"))
    return render_template("home")

#@login_required
@bp.get("/")
def index():
    users = auth.list_users()
    return render_template("users/index.html", users=users)

@has_permissions("user_new")
@bp.post("/create")
def create():
    if request.method == "POST":
        params = request.form
        _ = auth.create_user(
            alias=params["alias"],
            email=params["email"],
            password=params["password"],
            role_id=params["role_id"],
        )
        return redirect(url_for("users.index"))
    return render_template("users/create.html")
