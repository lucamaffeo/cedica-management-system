from src.core.database import db
from src.core.models.role import Role

def list_roles():
    roles = Role.query.all()
    return roles

def create_role(**kwargs):
    role = Role(**kwargs)
    db.session.add(role)
    db.session.commit()

    return role


