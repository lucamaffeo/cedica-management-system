from flask import current_app
from src.core.repositories import employee as employee_repo
from src.core.database import db
from src.core.models.horse import Horse
from src.core.repositories import document as document_repository


def list_horses(search='', assigned_activities_ja=None, sort_by='name', direction='asc', page=1):
    """
    Lista los caballos con filtros opcionales por nombre, actividades asignadas y ordenamiento.

    :param search: Nombre del caballo para buscar.
    :param assigned_activities_ja: Actividades asignadas para filtrar.
    :param sort_by: Campo por el cual ordenar los resultados.
    :param direction: Dirección del ordenamiento ('asc' o 'desc').
    :param page: Número de página para la paginación.
    :return: Caballos paginados según los filtros aplicados.
    """
    query = Horse.query

    if search:
        query = query.filter(
            (Horse.name.ilike(f"%{search}%"))
        )
    if assigned_activities_ja:
        query = query.filter(Horse.assigned_activities_ja ==
                             assigned_activities_ja)

    items_per_page = current_app.config.get('ITEMS_PER_PAGE')

    if sort_by in ['name', 'birth_date', 'entry_date']:
        if direction == 'asc':
            query = query.order_by(getattr(Horse, sort_by).asc())
        else:
            query = query.order_by(getattr(Horse, sort_by).desc())
    pagination_horses = query.paginate(
        page=page, per_page=items_per_page, error_out=False)

    return pagination_horses


def get_activities():
    """
    Obtiene las actividades asignadas disponibles.

    :return: Lista de actividades asignadas.
    """
    return Horse.assigned_activities_ja.property.columns[0].type.enums


def get_genders():
    """
    Obtiene los géneros disponibles.

    :return: Lista de géneros.
    """
    return Horse.gender.property.columns[0].type.enums


def get_purchase_donation():
    """
    Obtiene las opciones de compra/donación disponibles.

    :return: Lista de opciones de compra/donación.
    """
    return Horse.purchase_donation.property.columns[0].type.enums


def find_horse_by_name(name):
    """
    Encuentra un caballo por su nombre.

    :param name: Nombre del caballo.
    :return: El caballo si se encuentra, None si no.
    """
    horse = Horse.query.filter(Horse.name == name).first()
    return horse


def find_horse_by_assigned_activities_ja(assigned_activities_ja):
    """
    Encuentra un caballo por sus actividades asignadas.

    :param assigned_activities_ja: Actividades asignadas del caballo.
    :return: El caballo si se encuentra, None si no.
    """
    horse = Horse.query.filter(
        Horse.assigned_activities_ja == assigned_activities_ja).first()
    return horse


def get_horse(id):
    """
    Obtiene un caballo por su ID.

    :param id: ID del caballo a obtener.
    :return: El caballo si se encuentra, None si no.
    """
    horse = Horse.query.filter(Horse.id == id).first()
    return horse


def create_horse(**kwargs):
    """
    Crea un nuevo caballo en la base de datos.

    :param kwargs: Argumentos para crear un nuevo caballo.
    :return: El caballo creado.
    """
    trainer_ids = kwargs.pop('trainer_ids', [])

    horse = Horse(**kwargs)
    db.session.add(horse)

    for trainer_id in trainer_ids:
        trainer = employee_repo.get_employee(trainer_id)
        if trainer:
            horse.association.append(trainer)

    db.session.commit()
    return horse


def update_horse(horse_id, **kwargs):
    """
    Actualiza un caballo existente en la base de datos.

    :param horse_id: ID del caballo a actualizar.
    :param kwargs: Argumentos para actualizar el caballo.
    :return: True si el caballo fue actualizado, False si no se encontró.
    """
    horse = Horse.query.filter(Horse.id == horse_id).first()
    if not horse:
        return False

    trainer_ids = kwargs.pop('trainer_ids', [])

    for key, value in kwargs.items():
        setattr(horse, key, value)

    horse.association = []
    for trainer_id in trainer_ids:
        trainer = employee_repo.get_employee(trainer_id)
        if trainer:
            horse.association.append(trainer)

    db.session.commit()
    return True


def delete_horse(horse_id):
    """
    Elimina un caballo de la base de datos.

    :param horse_id: ID del caballo a eliminar.
    :return: True si el caballo fue eliminado, False si no se encontró.
    """
    horse = Horse.query.filter(Horse.id == horse_id).first()
    if horse:
        if horse.documents:
            for document in horse.documents:
                document_repository.delete_document(document.id)
        db.session.delete(horse)
        db.session.commit()
        return True
    return False
