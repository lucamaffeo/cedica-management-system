from src.core.database import db
from src.core.models.day import Day


def list_days():
    """
    Lista todos los días.

    Returns:
        list: Lista de todos los días.
    """
    days = Day.query.all()
    return days


def get_day(id):
    """
    Recupera un día por ID.

    Args:
        id (int): El ID del día.

    Returns:
        Day: El objeto día o None si no se encuentra.
    """
    day = Day.query.filter(Day.id == id).first()
    return day


def get_days(ids):
    """
    Recupera días por una lista de IDs.

    Args:
        ids (list): Lista de IDs de días.

    Returns:
        list: Lista de objetos día.
    """
    days = Day.query.filter(Day.id.in_(ids)).all()
    return days


def create_day(**kwargs):
    """
    Crea un nuevo día y lo agrega a la base de datos.

    Args:
        **kwargs: Argumentos de palabra clave para los atributos del día.

    Returns:
        Day: El objeto día creado.
    """
    day = Day(**kwargs)
    db.session.add(day)
    db.session.commit()

    return day
