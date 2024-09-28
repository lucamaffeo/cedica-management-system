from functools import wraps
import logging
from flask import session, abort

from src.core import auth
from src.core.models.user import User

logger = logging.getLogger(__name__)

def is_authenticated(session):
    return session.get("user") != None


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user") is None:
            return abort(401)
        return f(*args, **kwargs)

    return decorated_function

# decorator receiving permission name, checking if user is authenticated
# if user is authenticated, checks if user role has the permission
def has_permission(permission):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not is_authenticated(session):
                return abort(401)
            user_id = session["user"]["id"]
            user = auth.get_user(user_id)
            if user.has_permission(permission):
                return f(*args, **kwargs)
            return abort(403)
        return decorated_function
    return decorator
