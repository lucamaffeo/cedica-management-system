from src.core.database import db
from src.core.models.tutor import Tutor

def list_tutors():
    tutors = Tutor.query.all()
    return tutors

def create_tutor(**kwargs):
    tutor = Tutor(**kwargs)
    db.session.add(tutor)
    db.session.commit()

    return tutor

