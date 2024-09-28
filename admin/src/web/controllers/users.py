from flask import Blueprint, redirect, render_template, request, url_for

from src.core import auth
from src.web.helpers.auth import has_permission

bp = Blueprint("users", __name__, url_prefix="/users")

# register
@bp.get("/register")
@has_permission("user_create")
def register():
    return render_template("users/form.html", is_update=False, title='Crear Usuario')

@bp.get("/<int:id>/update")
@has_permission("user_update")
def edit(id):
    user = auth.get_user(id)
    return render_template("users/form.html", is_update=True, title='Actualizar Usuario', user=user)

@bp.get("/<int:id>/show")
@has_permission("user_show")
def show(id):
    user = auth.get_user(id)
    return render_template("users/show.html", user=user)

@bp.post("/<int:id>/update")
@has_permission("user_update")
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

@bp.get("/<int:id>/delete")
@has_permission("user_destroy")
def delete(id):
    auth.delete_user(id)
    return redirect(url_for("users.index"))

@bp.get("/")
@has_permission("user_index")
def index():
    search = request.args.get('search', '')
    role_filter = request.args.get('role_id', None)
    sort_by = request.args.get('sort_by', 'alias')
    direction = request.args.get('direction', 'asc')
    active = request.args.get('active', None)
    page = request.args.get('page', 1, type=int)  # Get the page number from query parameters

    # Pass the parameters to the `list_users` function
    users = auth.list_users(search, role_filter, sort_by, direction, active, page)

    return render_template("users/index.html", pagination=users)

@bp.post("/create")
@has_permission("user_create")
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
