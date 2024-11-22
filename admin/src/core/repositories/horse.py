from flask import current_app
from src.core.repositories import employee as employee_repo
from src.core.database import db
from src.core.models.horse import Horse
from src.core.repositories import document as document_repository


def list_horses(search='', assigned_activities_ja=None, sort_by='name', direction='asc', page=1):
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
    return Horse.assigned_activities_ja.property.columns[0].type.enums


def get_genders():
    return Horse.gender.property.columns[0].type.enums


def get_purchase_donation():
    return Horse.purchase_donation.property.columns[0].type.enums


def find_horse_by_name(name):
    horse = Horse.query.filter(Horse.name == name).first()
    return horse


def find_horse_by_assigned_activities_ja(assigned_activities_ja):
    horse = Horse.query.filter(
        Horse.assigned_activities_ja == assigned_activities_ja).first()
    return horse


def get_horse(id):
    horse = Horse.query.filter(Horse.id == id).first()
    return horse


def create_horse(**kwargs):
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
    horse = Horse.query.filter(Horse.id == horse_id).first()
    if horse:
        if horse.documents:
            for document in horse.documents:
                document_repository.delete_document(document.id)
        db.session.delete(horse)
        db.session.commit()
        return True
    return False
