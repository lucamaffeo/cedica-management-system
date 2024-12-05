from flask import Blueprint, redirect, render_template, request, session, url_for, flash
from src.core.validation.models.user import UserValidator
from src.core.repositories import user as auth
from src.core.repositories import role
from src.web.helpers.auth import has_permission
from src.web.helpers.flash import flash_validation_errors

bp = Blueprint("users", __name__, url_prefix="/users")

# Register


@bp.get("/create")
@has_permission("user_create")
def register():
    return render_template("users/form.html", is_update=False, title='Crear Usuario', roles=role.list_roles())

# Create user


@bp.post("/create")
@has_permission("user_create")
def create():
    data = request.form.to_dict()
    validator = UserValidator()

    errors = validator.validate(data)
    if errors:
        flash_validation_errors(errors)
        return redirect(url_for("users.create"))

    auth.create_user(
        alias=data["alias"],
        email=data["email"],
        password=data["password"],
        role_id=data["role_id"],
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
    return render_template("users/form.html", is_update=True, title='Actualizar Usuario', user=user, roles=role.list_roles())


@bp.route("/<int:id>/update", methods=["POST", "PATCH"])
def update(id):
    # Check if the current user has permission to update another user's profile
    is_update_own = id == session["user_id"]

    if not is_update_own:
        has_permission("user_update")(lambda: None)()

    data = request.form.to_dict()

    # Validate password match if being updated
    if data.get("password") and data.get("new_password"):
        if data.get("password") != data.get("new_password"):
            flash("Las contraseñas no coinciden.", "error")
            return redirect(url_for("users.update", id=id))
        # Use single password field for validator
        data['password'] = data.get("password")

    # Initialize validator with appropriate settings
    validator = UserValidator(
        user_id=id,
        check_password=bool(data.get('password')),
        is_update_own=is_update_own
    )

    errors = validator.validate_for_update(data)
    if errors:
        flash_validation_errors(errors)
        return redirect(url_for("users.update", id=id))

    # Prepare update data
    update_data = {
        "alias": data.get("alias"),
        "password": data.get("password") if data.get("password") else None,
        "active": 'active' in data if not is_update_own else None,
        "role_id": data.get("role_id") if not is_update_own else None
    }

    # Remove None values
    update_data = {k: v for k, v in update_data.items() if v is not None}

    if auth.update_user(id=id, **update_data):
        flash("Usuario actualizado con éxito.", "success")
        return redirect(url_for("users.index"))
    else:
        flash("Usuario no encontrado.", "error")
        return redirect(url_for("users.index"))

# Edit own profile


@bp.get("/profile/update")
def edit_profile():
    id = session["user_id"]
    user = auth.get_user(id)
    if not user:
        flash("Usuario no encontrado.", "error")
        return redirect(url_for("home"))
    return render_template("users/form.html", is_update_own=True, title='Actualizar Perfil', user=user)


@bp.post("/profile/update")
def update_profile():
    id = session["user_id"]
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
    user = auth.get_user(session["user_id"])
    if not user:
        flash("Usuario no encontrado.", "error")
        return redirect(url_for("home"))
    return render_template("users/show.html", user=user)


# Delete user
@bp.get("/<int:id>/delete")
@has_permission("user_destroy")
def delete(id):
    if id == session["user_id"]:
        flash("No puedes eliminarte a ti mismo.", "error")
        return redirect(url_for("users.index"))

    if auth.delete_user(id):
        flash("Usuario eliminado con éxito.", "info")
        return redirect(url_for("users.index"))
    else:
        flash("Usuario no encontrado o no puede ser borrado.", "error")
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

    users = auth.list_users(search, role_filter,
                            sort_by, direction, active, page)

    if not users.items:
        flash("No se encontraron usuarios.", "info")
    return render_template("users/index.html", pagination=users, roles=role.list_roles())
