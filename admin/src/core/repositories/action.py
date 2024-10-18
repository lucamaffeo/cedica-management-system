from src.core.database import db
from src.core.models.action import Action

def list_actions():
    actions = Action.query.all()
    return actions

def create_action(**kwargs):
    action = Action(**kwargs)
    db.session.add(action)
    db.session.commit()

    return action