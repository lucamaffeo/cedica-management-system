from flask import Blueprint, flash, redirect, render_template, request, session, url_for

from src.core import auth

bp= Blueprint("auth", __name__, url_prefix="/auth")



@bp.get("/")
def login():
    return render_template("auth/login.html")


@bp.post("/authenticate")
def authenticate():
    params = request.form

    user = auth.find_user_by_email_and_password(params["email"], params["password"])

    if not user:
        flash("Usuario o contraseña incorrecta", "error")

        return redirect(url_for("auth.login"))
    
    session["user"] = user.emial
    flash("¡La sesion se inicio correctamente!", "succes")

    return redirect(url_for("issues.index"))

@bp.get("/logout")
def logout():
    pass