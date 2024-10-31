from flask import current_app
from src.core.models.employee import Employee
from src.core.database import db
from src.core.models.horse import Horse


def list_horses(search='', assigned_activities_ja=None, sort_by='name', direction='asc', page=1):
    query = Horse.query

    if search:
       query= query.filter(
            (Horse.name.ilike(f"%{search}%")) 
        )
    if assigned_activities_ja:
       query = query.filter(Horse.assigned_activities_ja == assigned_activities_ja)
    else:
        query = query

    items_per_page = current_app.config.get('ITEMS_PER_PAGE')

    if sort_by in ['name', 'birth_date', 'entry_date']:
        if direction == 'asc':
            query = query.order_by(getattr(Horse, sort_by).asc())
        else:
            query = query.order_by(getattr(Horse, sort_by).desc())
    pagination_horses = query.paginate(page=page, per_page=items_per_page, error_out=False)

    return pagination_horses

def find_horse_by_name(name):
    horse = Horse.query.filter(Horse.name == name).first()
    return horse

def find_horse_by_assigned_activities_ja(assigned_activities_ja):
    horse = Horse.query.filter(Horse.assigned_activities_ja == assigned_activities_ja).first()
    return horse

def get_horse(id):
    horse = Horse.query.filter(Horse.id == id).first()
    return horse

def create_horse(**kwargs):
    horse = Horse(**kwargs)
    db.session.add(horse)
    db.session.commit()
    return horse

def update_horse(horse_id, **kwargs):
    horse = Horse.query.filter(Horse.id == horse_id).first()
    for key, value in kwargs.items():
        setattr(horse, key, value)
    db.session.commit()
    return horse

def delete_horse(horse_id):
    horse = Horse.query.filter(Horse.id == horse_id).first()
    db.session.delete(horse)
    db.session.commit()
    return horse

