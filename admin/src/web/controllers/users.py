from flask import Blueprint, redirect, render_template, request, url_for

from src.core import auth
from src.web.helpers.auth import has_permission

bp = Blueprint("users", __name__, url_prefix="/users")

# register
@has_permission("user_create")
@bp.get("/register")
def register():
    return render_template("users/form.html", is_update=False, title='Crear Usuario')

@has_permission("user_update")
@bp.get("/<int:id>/update")
def edit(id):
    user = auth.get_user(id)
    return render_template("users/form.html", is_update=True, title='Actualizar Usuario', user=user)

@has_permission("user_show")
@bp.get("/<int:id>/show")
def show(id):
    user = auth.get_user(id)
    return render_template("users/show.html", user=user)

@has_permission("user_update")
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

@has_permission("user_destroy")
@bp.get("/<int:id>/delete")
def delete(id):
    auth.delete_user(id)
    return redirect(url_for("users.index"))

@has_permission("user_index")
@bp.get("/")
def index():
    search = request.args.get('search', '')
    role_filter = request.args.get('role', None)
    sort_by = request.args.get('sort_by', 'alias')
    direction = request.args.get('direction', 'asc')

    # Pasar los parámetros a la función `list_users`
    users = auth.list_users(search, role_filter, sort_by, direction)

    return render_template("users/index.html", users=users)

@has_permission("user_create")
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
