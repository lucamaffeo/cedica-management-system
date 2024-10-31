from flask import current_app
from src.core.database import db
from src.core.models.rider import Rider

def create_rider(**kwargs):
    rider = Rider(**kwargs)
    db.session.add(rider)
    db.session.commit()

    return rider

def list_riders(search='', sort_by='name', direction='asc', page=1):
    query = Rider.query

    if search:
        query = query.filter(
            (Rider.name.ilike(f'%{search}%')) |
            (Rider.surname.ilike(f'%{search}%')) |
            (Rider.dni.ilike(f'%{search}%')) |
            (Rider.professionals.ilike(f'%{search}%'))
        )

    query = query  # No aplicar filtro, mostrar todos

    items_per_page = current_app.config.get('ITEMS_PER_PAGE')

    # Aplicar ordenación
    if sort_by in ['name', 'surname']:
        if direction == 'asc':
            query = query.order_by(getattr(Rider, sort_by).asc())
        else:
            query = query.order_by(getattr(Rider, sort_by).desc())

    pagination_riders = query.paginate(page=page, per_page=items_per_page, error_out=False)

    return pagination_riders

def find_rider_by_name(name):
    rider = Rider.query.filter(Rider.name == name).first()
    return rider

def find_rider_by_apellido(surname):
    rider = Rider.query.filter(Rider.surname == surname).first()
    return rider

def find_rider_by_dni(dni):
    rider = Rider.query.filter(Rider.dni == dni).first()
    return rider

def find_rider_by_professionals(professionals):
    rider = Rider.query.filter(Rider.professionals == professionals).first()
    return rider

def update_rider(id, **kwargs):
    rider = Rider.query.filter(Rider.id == id).first()
    if not rider:
        return None
    for key, value in kwargs.items():
        setattr(rider, key, value)
    db.session.commit()
    return rider

def delete_rider(id):
    rider = Rider.query.filter(Rider.id == id).first()
    db.session.delete(rider)
    db.session.commit()

def get_rider(id):
    rider = Rider.query.filter(Rider.id == id).first()
    return rider

def has_assignment(rider, assignment_name):
    return any(assignment.name == assignment_name for assignment in rider.assignments)
