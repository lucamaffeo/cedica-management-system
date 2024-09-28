from src.core.database import db
from src.core.models.permission import Permission
from src.core.models.role import Role
from src.core.models.user import User
from src.core.models.employee import Employee

from werkzeug.security import generate_password_hash

def list_users(search='', role_filter=None, sort_by='alias', direction='asc'):
    # Inicializar la consulta de base de datos
    query = User.query

    # Aplicar búsqueda si el parámetro 'search' no está vacío
    if search:
        query = query.filter(User.email.ilike(f'%{search}%'))

    # Aplicar filtro de rol si el parámetro 'role' no es None o vacío
    if role_filter:
        query = query.filter_by(role_id=role_filter)

    # Aplicar ordenación
    if direction == 'asc':
        query = query.order_by(getattr(User, sort_by).asc())
    else:
        query = query.order_by(getattr(User, sort_by).desc())

    return query.all()

def create_user(**kwargs):
    if 'password' in kwargs:
        kwargs['password'] = generate_password_hash(kwargs['password'])
    user = User(**kwargs)
    db.session.add(user)
    db.session.commit()

    return user

def update_user(id, **kwargs):
    user = User.query.filter(User.id == id).first()
    for key, value in kwargs.items():
        setattr(user, key, value)
    db.session.commit()
    return user

def delete_user(id):
    user = User.query.filter(User.id == id).first()
    db.session.delete(user)
    db.session.commit()

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

def get_user(id):
    user = User.query.filter(User.id == id).first()
    return user

def find_user_by_email(email):
    return User.query.filter(User.email == email).first()


def find_user_by_active():
   return User.query.filter(User.active == True).all()


def find_user_by_role(role_id):
    return User.query.filter(User.role_id == role_id).all()
