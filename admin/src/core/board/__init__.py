from src.core.board.permission import Permission
from src.core.board.role import Role
from src.core.database import db
from src.core.auth.user import User
from src.core.board.employee import Employee

from sqlalchemy import text
from werkzeug.security import generate_password_hash

def create_employee(**kwargs):
    employee = Employee(**kwargs)
    db.session.add(employee)
    db.session.commit()

    return employee

def list_employees():
    employees = Employee.query.all()
    return employees