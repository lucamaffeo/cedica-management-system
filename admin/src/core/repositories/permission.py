from src.core.database import db
from src.core.models.permission import Permission

def create_permission(**kwargs):
    permission = Permission(**kwargs)
    db.session.add(permission)
    db.session.commit()

    return permission

