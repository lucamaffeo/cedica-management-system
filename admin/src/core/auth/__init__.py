from src.core.database import db
from src.core.auth.user import User

def list_users():
    users = User.query.all()

    return users

def create_user(**kwargs):
    user = User(**kwargs)
    db.session.add(user)
    db.session.commit()

    return user

def find_user_by_email_and_password(email, password):
    user = User.query.filter_by(email=email, password=password).first()

    return user

