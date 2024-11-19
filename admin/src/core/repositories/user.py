from flask import current_app
from sqlalchemy import and_, exists
from src.core.database import db
from src.core.models.user import User
from src.core.models.role import Role
from src.core.models.permission import Permission

from werkzeug.security import generate_password_hash

def list_users(search='', role_id=None, sort_by='alias', direction='asc', active=None, page=1):
    # Inicializar la consulta de base de datos
    query = User.query

    # Aplicar búsqueda si el parámetro 'search' no está vacío
    if search:
        query = query.filter(User.email.ilike(f'%{search}%'))

    # Aplicar filtro de rol si el parámetro 'role' no es None o vacío
    if role_id:
        query = query.filter_by(role_id=role_id)

    items_per_page = current_app.config.get('ITEMS_PER_PAGE')

    # Aplicar filtro de estado activo si el parámetro 'active' no es None
    if active is not None and active != '':  # Verifica que active no sea None ni vacío
        # Convierte el string 'true' o 'false' a booleano
        active_value = active == 'true'
        query = query.filter_by(active=active_value)
    # Aplicar ordenación
    if direction == 'asc':
        query = query.order_by(getattr(User, sort_by).asc())
    else:
        query = query.order_by(getattr(User, sort_by).desc())

    paginated_users = query.paginate(page=page, per_page=items_per_page, error_out=False)

    return paginated_users

def create_user(**kwargs):
    if 'password' in kwargs:
        kwargs['password'] = generate_password_hash(kwargs['password'])
    user = User(**kwargs)
    db.session.add(user)
    db.session.commit()

    return user

def update_user(id, **kwargs):
    user = User.query.filter(User.id == id).first()
    if not user:
        return False
    if 'password' in kwargs and kwargs['password'] is not None:
        kwargs['password'] = generate_password_hash(kwargs['password'])
    else:
        kwargs.pop('password', None)
    for key, value in kwargs.items():
        setattr(user, key, value)
    db.session.commit()
    return True

def delete_user(id):
    user = User.query.filter(User.id == id).first()
    if user:
        db.session.delete(user)
        db.session.commit()
        return True
    return False

def get_user(id) -> User | None:
    user = User.query.filter(User.id == id).first()
    return user

def find_user_by_email(email):
    return User.query.filter(User.email == email).first()


def find_user_by_active():
   return User.query.filter(User.active == True).all()


def find_user_by_role(role_id):
    return User.query.filter(User.role_id == role_id).all()

def has_permission(user_id: int, permission: str) -> bool:
    """
    Check if a user has a specific permission using a parameterized query.
    This is more efficient than loading all permissions into memory.


    Args:
        user_id: The ID of the user to check
        permission: The permission name to check

    Returns:
        bool: True if user has the permission, False otherwise
    """
    return db.session.query(exists().where(
        and_(
            User.id == user_id,
            User.role_id == Role.id,
            Role.permissions.any(Permission.name == permission)
        )
    )).scalar()

def list_unassociated_users():
    return User.query.filter(~User.employee.any()).all()
