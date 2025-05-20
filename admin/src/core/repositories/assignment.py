from src.core.database import db
from src.core.models.assignment import Assignment

def list_assignments():
    """
    Lista todas las asignaciones disponibles.

    :return: Lista de asignaciones.
    """
    assignments = Assignment.query.all()
    return assignments

def create_assignment(**kwargs):
    """
    Crea una nueva asignación en la base de datos.

    :param kwargs: Argumentos para crear una nueva asignación.
    :return: La asignación creada.
    """
    assignment = Assignment(**kwargs)
    db.session.add(assignment)
    db.session.commit()

    return assignment

def get_assignment_ids_by_names(names):
    """
    Obtiene los IDs de las asignaciones por sus nombres.

    :param names: Lista de nombres de asignaciones.
    :return: Lista de IDs de las asignaciones.
    """
    assignments = Assignment.query.filter(Assignment.name.in_(names)).all()
    return [assignment.id for assignment in assignments]

def get_assignments(ids):
    """
    Obtiene las asignaciones por sus IDs.

    :param ids: Lista de IDs de asignaciones.
    :return: Lista de asignaciones.
    """
    assignments = Assignment.query.filter(Assignment.id.in_(ids)).all()
    return assignments

