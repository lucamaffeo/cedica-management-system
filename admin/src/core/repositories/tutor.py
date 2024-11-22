from src.core.database import db
from src.core.models.tutor import Tutor
from src.core.models.rider import rider_tutor


def list_tutors():
    tutors = Tutor.query.all()
    return tutors


def get_tutor(id):
    tutor = Tutor.query.filter(Tutor.id == id).first()
    return tutor


def get_tutors_with_relationships(id):
    tutors_with_relationship = db.session.query(
        Tutor, rider_tutor.c.relationship
    ).join(
        rider_tutor, Tutor.id == rider_tutor.c.tutor_id
    ).filter(
        rider_tutor.c.rider_id == id
    ).all()
    return tutors_with_relationship


def create_tutor(**kwargs):
    tutor = Tutor(**kwargs)
    db.session.add(tutor)
    db.session.commit()

    return tutor
