from src.core.database import db
from src.core.models.horse import Horse


def list_Horse(page, per_page, filters=None):
    query = Horse.query

    if filters:
        if 'name' in filters:
                query = query.filter(Horse.name.ilike(f"%{filters['name']}%"))
        if 'assigned_activities_ja' in filters:
                query = query.filter(Horse.assigned_activities_ja == filters['assigned_activities_ja'])
    return query.paginate(page=page, per_page=per_page)

def get_horse_by_id(horse_id):
    return Horse.query.get(horse_id)

def create_horse(**kwargs):
    horse = Horse(**kwargs)
    db.session.add(horse)
    db.session.commit()
    return horse

def update_horse(horse_id, **kwargs):
    horse = Horse.query.get(horse_id)
    for key, value in kwargs.items():
        setattr(horse, key, value)
    db.session.commit()
    return horse

def delete_horse(horse_id):
    horse = Horse.query.get(horse_id)
    db.session.delete(horse)
    db.session.commit()
    return horse
