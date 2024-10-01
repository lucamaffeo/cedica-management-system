from src.core.database import db
from src.core.models.employee import Employee

def create_employee(**kwargs):
    employee = Employee(**kwargs)
    db.session.add(employee)
    db.session.commit()

    return employee

def list_employees():
    employees = Employee.query.all()
    return employees

