from flask import Blueprint, flash, redirect, render_template, request, session, url_for
from src.core.models.user import User
from werkzeug.security import check_password_hash
from src.core.repositories import user as auth

bp = Blueprint("auth", __name__, url_prefix="/auth")


@bp.get("/")
def login():
    return render_template("auth/login.html")


@bp.post("/authenticate")
def authenticate():
    params = request.form
    
    # Check if email and password are present
    email = params.get("email")
    password = params.get("password")
    
    if not email or not password:
        flash("Tanto el correo electrónico como la contraseña son obligatorios.", "error")
        return redirect(url_for("auth.login"))

    # Find user by email
    user: User | None = auth.find_user_by_email(email)

    if not user or not user.active or not check_password_hash(user.password, password):
        flash("Usuario o clave incorrecto o cuenta inactiva.", "error")
        return redirect(url_for("auth.login"))

    # Set session for user
    session["user_id"] = user.id
    flash("La sesión se inició correctamente.", "success")

    return redirect(url_for("home"))


@bp.get("/logout")
def logout():
    session.clear()  # Clears all session data
    flash("La sesión se cerró correctamente.", "info")

    return redirect(url_for("home"))
