from src.core.database import db
from src.core.models.day import Day


def list_days():
    days = Day.query.all()
    return days


def get_day(id):
    day = Day.query.filter(Day.id == id).first()
    return day


def get_days(ids):
    days = Day.query.filter(Day.id.in_(ids)).all()
    return days


def create_day(**kwargs):
    day = Day(**kwargs)
    db.session.add(day)
    db.session.commit()

    return day
