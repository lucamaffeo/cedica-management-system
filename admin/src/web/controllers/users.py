from flask import Blueprint, redirect, render_template, request, session, url_for, flash
from src.core.repositories import user as auth
from src.web.helpers.auth import has_permission

bp = Blueprint("users", __name__, url_prefix="/users")

# Register
@bp.get("/register")
@has_permission("user_create")
def register():
    return render_template("users/form.html", is_update=False, title='Crear Usuario')

# Create user
@bp.post("/register")
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

# Edit user
@bp.get("/<int:id>/update")
@has_permission("user_update")
def edit(id):
    user = auth.get_user(id)
    if not user:
        flash("Usuario no encontrado.", "error")
        return redirect(url_for("users.index"))
    return render_template("users/form.html", is_update=True, title='Actualizar Usuario', user=user)

@bp.route("/<int:id>/update", methods=["POST", "PATCH"])
def update(id):
    # Check if the current user has permission to update another user's profile
    is_update_own = id == session["user"]["id"]

    if not is_update_own:
        has_permission("user_update")(lambda: None)()

    # Get the current user object
    user = auth.get_user(id)
    if not user:
        flash("Usuario no encontrado.", "error")
        return redirect(url_for("users.index"))

    # Extract the form data
    params = request.form

    # If password is being updated, ensure the new passwords match
    if params.get("password") and params.get("new_password"):
        if params.get("password") != params.get("new_password"):
            flash("Las contraseñas no coinciden.", "error")
            return redirect(url_for("users.update", id=id))

    # Prepare the parameters for the update
    update_data = {
        "alias": params.get("alias"),
        "email": params.get("email"),
        "password": params.get("password") if params.get("password") and params.get("new_password") else None,
        "active": 'active' in params if not is_update_own else None,
        "role_id": params.get("role_id") if not is_update_own else None
    }

    # Remove any None values to prevent overwriting fields unintentionally
    update_data = {k: v for k, v in update_data.items() if v is not None}

    # Call the update_user function from the repository
    auth.update_user(id=id, **update_data)

    flash("Usuario actualizado con éxito.", "success")
    return redirect(url_for("users.index"))

# Edit own profile
@bp.get("/profile/update")
def edit_profile():
    id = session["user"]["id"]
    user = auth.get_user(id)
    if not user:
        flash("Usuario no encontrado.", "error")
        return redirect(url_for("home"))
    return render_template("users/form.html", is_update_own=True, title='Actualizar Perfil', user=user)

@bp.post("/profile/update")
def update_profile():
    id = session["user"]["id"]
    update(id)
    return redirect(url_for("users.profile"))

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

