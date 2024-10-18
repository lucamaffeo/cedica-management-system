from src.core.database import db
from src.core.models.assignment import Assignment

def create_assignment(**kwargs):
    assignment = Assignment(**kwargs)
    db.session.add(assignment)
    db.session.commit()

    return assignment

