from functools import wraps
from flask import session, abort, request

from src.core.models.user import User

def is_authenticated(session):
    return session.get("user") != None


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user") is None:
            return abort(401)
        return f(*args, **kwargs)

    return decorated_function

def has_permission(permission):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            user: User = session.get("user")
            if user.has_permission(permission):
                return f(*args, **kwargs)
            return abort(403)
        return decorated_function
    return decorator

