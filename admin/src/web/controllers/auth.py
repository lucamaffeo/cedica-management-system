from flask import Blueprint, current_app, flash, redirect, render_template, request, session, url_for
from src.core.models.user import User
from werkzeug.security import check_password_hash
from src.core.repositories import user as auth
from google.oauth2.id_token import verify_oauth2_token
from google.auth.transport import requests
from google_auth_oauthlib.flow import Flow

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
    session.permanent = True
    session["user_id"] = user.id
    flash("La sesión se inició correctamente.", "success")
    return redirect(url_for("home"))


@bp.get("/logout")
def logout():
    session.clear()  # Clears all session data
    flash("La sesión se cerró correctamente.", "info")
    return redirect(url_for("home"))


class GoogleOAuth:
    def __init__(self, client_secrets_file, oauth_scopes, redirect_uri):
        self.client_secrets_file = client_secrets_file
        self.oauth_scopes = oauth_scopes
        self.redirect_uri = redirect_uri
        self.flow = Flow.from_client_secrets_file(
            self.client_secrets_file,
            scopes=self.oauth_scopes,
            redirect_uri=self.redirect_uri
        )

    def get_authorization_url(self):
        return self.flow.authorization_url()

    def fetch_token(self, authorization_response):
        self.flow.fetch_token(authorization_response=authorization_response)

    def verify_id_token(self):
        return verify_oauth2_token(
            self.flow.credentials.id_token,
            requests.Request(),
            self.flow.client_config['client_id']
        )


@bp.get("/google/login")
def google_login():
    """Initiate Google OAuth flow"""
    # Configuration for Google OAuth
    GOOGLE_CLIENT_SECRETS_FILE = current_app.config.get(
        "GOOGLE_CLIENT_SECRETS_FILE")
    GOOGLE_OAUTH_SCOPES = current_app.config.get("GOOGLE_OAUTH_SCOPES")
    REDIRECT_URI = current_app.config.get("GOOGLE_REDIRECT_URI")

    google_oauth = GoogleOAuth(
        GOOGLE_CLIENT_SECRETS_FILE, GOOGLE_OAUTH_SCOPES, REDIRECT_URI)

    email = request.args.get('email')
    if not email:
        flash("El correo electrónico es obligatorio.", "error")
        return redirect(url_for("auth.login"))

    # Check if user exists in your database
    user: User | None = auth.find_user_by_email(email)
    if not user or not user.active:
        flash("No existe una cuenta activa con este correo electrónico.", "error")
        return redirect(url_for("auth.login"))

    # Store email in session for verification after OAuth
    session['pending_google_email'] = email

    # Generate OAuth URL and redirect to Google
    authorization_url, state = google_oauth.get_authorization_url()
    session["state"] = state
    return redirect(authorization_url)


@bp.get("/google/callback")
def google_callback():
    """Handle the OAuth 2.0 callback from Google"""
    try:
        # Get the expected email from session
        expected_email = session.pop('pending_google_email', None)
        if not expected_email:
            flash("La sesión de autenticación ha expirado.", "error")
            return redirect(url_for("auth.login"))

        # Configuration for Google OAuth
        GOOGLE_CLIENT_SECRETS_FILE = current_app.config.get(
            "GOOGLE_CLIENT_SECRETS_FILE")
        GOOGLE_OAUTH_SCOPES = current_app.config.get("GOOGLE_OAUTH_SCOPES")
        REDIRECT_URI = current_app.config.get("GOOGLE_REDIRECT_URI")

        google_oauth = GoogleOAuth(
            GOOGLE_CLIENT_SECRETS_FILE, GOOGLE_OAUTH_SCOPES, REDIRECT_URI)

        # Get the authorization code from Google
        google_oauth.fetch_token(authorization_response=request.url)

        # Get the credentials and ID token
        id_info = google_oauth.verify_id_token()

        # Get email from Google response
        google_email = id_info.get('email')

        # Verify emails match
        if google_email != expected_email:
            flash(
                "El correo electrónico de Google no coincide con el proporcionado.", "error")
            return redirect(url_for("auth.login"))

        # Get user from database
        user: User | None = auth.find_user_by_email(google_email)
        if not user or not user.active:
            flash("Usuario no encontrado o cuenta inactiva.", "error")
            return redirect(url_for("auth.login"))

        # Set session for user
        session.permanent = True
        session["user_id"] = user.id
        flash("La sesión se inició correctamente con Google.", "success")
        return redirect(url_for("home"))

    except Exception as e:
        flash(f"Error al autenticar con Google: {str(e)}", "error")
        return redirect(url_for("auth.login"))
