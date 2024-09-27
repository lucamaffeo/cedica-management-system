from src.core.database import db
from src.core.models.permission import Permission
from src.core.models.role import Role
from src.core.models.user import User
from src.core.models.employee import Employee

from sqlalchemy import text
from werkzeug.security import generate_password_hash

def list_users():
    users = User.query.all()

    return users

def create_user(**kwargs):
    if 'password' in kwargs:
        kwargs['password'] = generate_password_hash(kwargs['password'])
    user = User(**kwargs)
    db.session.add(user)
    db.session.commit()

    return user

def list_roles():
    roles = Role.query.all()
    return roles

def create_role(**kwargs):
    role = Role(**kwargs)
    db.session.add(role)
    db.session.commit()

    return role

def create_permission(**kwargs):
    permission = Permission(**kwargs)
    db.session.add(permission)
    db.session.commit()

    return permission

def create_employee(**kwargs):
    employee = Employee(**kwargs)
    db.session.add(employee)
    db.session.commit()

    return employee

def list_employees():
    employees = Employee.query.all()
    return employees

def find_user_by_email(email):
    return User.query.filter(User.email == email).first()


def find_user_by_active():
   return User.query.filter(User.activo == True).all()


def find_user_by_role(role_id):
    return User.query.filter(User.role_id == role_id).all()
