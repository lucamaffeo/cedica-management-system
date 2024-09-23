from flask import Blueprint, flash, redirect, render_template, request, session, url_for, g

from src.core import auth

bp = Blueprint("auth", __name__, url_prefix="/auth")


@bp.get("/")
def login():
    return render_template("auth/login.html")


@bp.post("/authenticate")
def authenticate():
    params = request.form

    user = auth.find_user_by_email_and_pass(params["email"], params["password"])

    if not user:
        flash("Usuario o clave incorrecto.", "error")
        return redirect(url_for("auth.login"))

    session["user"] = user.email
    flash("La sesión se inició correctamente.", "success")

    return redirect(url_for("home"))


@bp.get("/logout")
def logout():
    del session["user"]
    session.clear()
    flash("La sesión se cerró correctamente.", "info")

    return redirect(url_for("auth.login"))

# SQLi
@bp.post("/authenticate_sqli")
def authenticate_sqli():
    params = request.form

    user = auth.find_user_by_email_and_pass_sqli(params['email'], params['password'])

    if not user:
        flash("Usuario o clave incorrecto.")
        return redirect(url_for('auth.login'))

    session['user'] = user.email
    flash("La sesión se inició correctamente.")

    return redirect(url_for('home'))