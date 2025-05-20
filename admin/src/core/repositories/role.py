from src.core.database import db
from src.core.models.role import Role


def list_roles():
    """
    Listar todos los roles.

    Returns:
        list: Lista de todos los roles.
    """
    roles = Role.query.all()
    return roles


def create_role(**kwargs):
    """
    Crear un nuevo rol.

    Args:
        **kwargs: Atributos del rol.

    Returns:
        Role: El rol creado.
    """
    role = Role(**kwargs)
    db.session.add(role)
    db.session.commit()

    return role


def get_role_by_id(role_id):
    """
    Obtener un rol por ID.

    Args:
        role_id (int): ID del rol.

    Returns:
        Role: El rol si se encuentra.
    """
    role = Role.query.get(role_id)
    return role
