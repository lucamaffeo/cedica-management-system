from src.core.database import db
from src.core.models.assignment import Assignment

def list_assignments():
    assignments = Assignment.query.all()
    return assignments

def create_assignment(**kwargs):
    assignment = Assignment(**kwargs)
    db.session.add(assignment)
    db.session.commit()

    return assignment

def get_assignment_ids_by_names(names):
    assignments = Assignment.query.filter(Assignment.name.in_(names)).all()
    return [assignment.id for assignment in assignments]

def get_assignments(ids):
    assignments = Assignment.query.filter(Assignment.id.in_(ids)).all()
    return assignments
