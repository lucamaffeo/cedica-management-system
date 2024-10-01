from flask import Blueprint, redirect, render_template, request, session, url_for, flash
from src.core.repositories import user as auth
from src.web.helpers.auth import has_permission

bp = Blueprint("users", __name__, url_prefix="/users")

# Register
@bp.get("/register")
@has_permission("user_create")
def register():
    return render_template("users/form.html", is_update=False, title='Crear Usuario')


# Edit user
@bp.get("/<int:id>/update")
@has_permission("user_update")
def edit(id):
    user = auth.get_user(id)
    if not user:
        flash("Usuario no encontrado.", "error")
        return redirect(url_for("users.index"))
    return render_template("users/form.html", is_update=True, title='Actualizar Usuario', user=user)

# Edit own profile
@bp.get("/profile/update")
def edit_profile():
    id = session["user"]["id"]
    user = auth.get_user(id)
    if not user:
        flash("Usuario no encontrado.", "error")
        return redirect(url_for("home"))
    return render_template("users/form.html", title='Actualizar Perfil', user=user)

# Show user
@bp.get("/<int:id>/show")
@has_permission("user_show")
def show(id):
    user = auth.get_user(id)
    if not user:
        flash("Usuario no encontrado.", "error")
        return redirect(url_for("users.index"))
    return render_template("users/show.html", user=user)

# Show profile
@bp.get("/profile")
def profile():
    id = session["user"]["id"]
    print(id)
    user = auth.get_user(id)
    if not user:
        flash("Usuario no encontrado.", "error")
        return redirect(url_for("home"))
    return render_template("users/show.html", user=user)

@bp.post("/<int:id>/update")
@has_permission("user_update")
def update(id):
    params = request.form
    user = auth.get_user(id)
    if not user:
        flash("Usuario no encontrado.", "error")
        return redirect(url_for("users.index"))

    if not params.get("password") or not params.get("new_password") or params.get("password") != params.get("new_password"):
        flash("Las contraseñas no coinciden o están vacías.", "error")
        return redirect(url_for("users.update", id=id))

    auth.update_user(
        id=id,
        alias=params.get("alias"),
        email=params.get("email"),
        password=params.get("password"),
        active='active' in params,
        role_id=params.get("role_id"),
    )

    flash("Usuario actualizado con éxito.", "success")
    return redirect(url_for("users.index"))



# Delete user
@bp.get("/<int:id>/delete")
@has_permission("user_destroy")
def delete(id):
    user = auth.get_user(id)
    if not user:
        flash("Usuario no encontrado.", "error")
        return redirect(url_for("users.index"))

    auth.delete_user(id)
    flash("Usuario eliminado con éxito.", "info")
    return redirect(url_for("users.index"))


# List users
@bp.get("/")
@has_permission("user_index")
def index():
    search = request.args.get('search', '')
    role_filter = request.args.get('role_id', None)
    sort_by = request.args.get('sort_by', 'alias')
    direction = request.args.get('direction', 'asc')
    active = request.args.get('active', None)
    page = request.args.get('page', 1, type=int)

    users = auth.list_users(search, role_filter, sort_by, direction, active, page)
    
    if not users.items:
        flash("No se encontraron usuarios.", "info")
    return render_template("users/index.html", pagination=users)


# Create user
@bp.post("/create")
@has_permission("user_create")
def create():
    params = request.form
    if not params.get("alias") or not params.get("email") or not params.get("password"):
        flash("Alias, correo electrónico y contraseña son obligatorios.", "error")
        return render_template("users/create.html")
    
    auth.create_user(
        alias=params["alias"],
        email=params["email"],
        password=params["password"],  # Make sure to hash the password in the core
        role_id=params["role_id"],
    )
    
    flash("Usuario creado con éxito.", "success")
    return redirect(url_for("users.index"))
