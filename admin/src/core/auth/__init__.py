from src.core.database import db
from src.core.auth.user import User

from sqlalchemy import text

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


def find_user_by_email_and_pass(email, password):
    return User.query.filter(User.email == email, User.password == password).first()


def find_user_by_email(email):
    return User.query.filter(User.email == email).first()

# SQLi
def find_user_by_email_and_pass_sqli(email, password):
    sql = text("SELECT * from users WHERE email = '"+email+"' AND password = '"+password+"'")
    return db.engine.execute(sql).first()