from flask import current_app
from src.core.database import db
from src.core.models.contact import Contact, ContactStatus


def list_contacts(sort_by='email', direction='asc', status_id=None, page=1):
    """
    Lista los contactos con filtros opcionales por estado y ordenamiento.

    :param sort_by: Campo por el cual ordenar los resultados.
    :param direction: Dirección del ordenamiento ('asc' o 'desc').
    :param status_id: ID del estado para filtrar.
    :param page: Número de página para la paginación.
    :return: Contactos paginados según los filtros aplicados.
    """
    query = Contact.query

    if status_id:
        query = query.filter(Contact.status_id == status_id)

    items_per_page = current_app.config.get('ITEMS_PER_PAGE')

    if direction == 'asc':
        query = query.order_by(getattr(Contact, sort_by).asc())
    else:
        query = query.order_by(getattr(Contact, sort_by).desc())

    paginated_contacts = query.paginate(
        page=page, per_page=items_per_page, error_out=False)

    return paginated_contacts


def list_statuses():
    """
    Lista todos los estados de contacto disponibles.

    :return: Lista de estados de contacto.
    """
    contact_status = ContactStatus.query.all()
    return contact_status


def create_contact(**kwargs):
    """
    Crea un nuevo contacto en la base de datos.

    :param kwargs: Argumentos para crear un nuevo contacto.
    :return: El contacto creado.
    """
    contact = Contact(**kwargs)
    db.session.add(contact)
    db.session.commit()

    return contact


def create_status(**kwargs):
    """
    Crea un nuevo estado de contacto en la base de datos.

    :param kwargs: Argumentos para crear un nuevo estado.
    :return: El estado creado.
    """
    status = ContactStatus(**kwargs)
    db.session.add(status)
    db.session.commit()
    return status


def update_contact(id, **kwargs):
    """
    Actualiza un contacto existente en la base de datos.

    :param id: ID del contacto a actualizar.
    :param kwargs: Argumentos para actualizar el contacto.
    :return: True si el contacto fue actualizado, False si no se encontró.
    """
    contact = Contact.query.filter(Contact.id == id).first()
    if not contact:
        return False
    for key, value in kwargs.items():
        if key == 'status_id' and value is None:
            continue
        setattr(contact, key, value)
    db.session.commit()
    return True


def delete_contact(id):
    """
    Elimina un contacto de la base de datos.

    :param id: ID del contacto a eliminar.
    :return: True si el contacto fue eliminado, False si no se encontró.
    """
    contact = Contact.query.filter(Contact.id == id).first()
    if contact:
        db.session.delete(contact)
        db.session.commit()
        return True
    return False


def get_contact(id) -> Contact | None:
    """
    Obtiene un contacto por su ID.

    :param id: ID del contacto a obtener.
    :return: El contacto si se encuentra, None si no.
    """
    contact = Contact.query.filter(Contact.id == id).first()
    return contact
