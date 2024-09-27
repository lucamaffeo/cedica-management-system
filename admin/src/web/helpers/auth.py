from functools import wraps
from flask import session, abort, request

def is_authenticated(session):
    return session.get("user") != None


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user") is None:
            return abort(401)
        return f(*args, **kwargs)

    return decorated_function

def has_permissions(permission):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            user_permissions = session.get("permissions", [])
            if permission not in user_permissions:
                return abort(403)
            return f(*args, **kwargs)
        return decorated_function
    return decorator

