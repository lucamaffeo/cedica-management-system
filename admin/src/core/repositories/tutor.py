from src.core.database import db
from src.core.models.tutor import Tutor
from src.core.models.rider import rider_tutor


def list_tutors():
    """
    Listar todos los tutores.

    Returns:
        list: Lista de todos los tutores.
    """
    tutors = Tutor.query.all()
    return tutors


def get_tutor(id):
    """
    Obtener un tutor por ID.

    Args:
        id (int): ID del tutor.

    Returns:
        Tutor: El tutor si se encuentra.
    """
    tutor = Tutor.query.filter(Tutor.id == id).first()
    return tutor


def get_tutors_with_relationships(id):
    """
    Obtener tutores con sus relaciones con un jinete específico.

    Args:
        id (int): ID del jinete.

    Returns:
        list: Lista de tutores con sus relaciones.
    """
    tutors_with_relationship = db.session.query(
        Tutor, rider_tutor.c.relationship
    ).join(
        rider_tutor, Tutor.id == rider_tutor.c.tutor_id
    ).filter(
        rider_tutor.c.rider_id == id
    ).all()
    return tutors_with_relationship


def create_tutor(**kwargs):
    """
    Crear un nuevo tutor.

    Args:
        **kwargs: Atributos del tutor.

    Returns:
        Tutor: El tutor creado.
    """
    tutor = Tutor(**kwargs)
    db.session.add(tutor)
    db.session.commit()

    return tutor
