from flask import current_app
from src.core.database import db
from src.core.models.employee import Employee
from src.core.repositories import document as document_repository


def create_employee(**kwargs):
    employee = Employee(**kwargs)
    db.session.add(employee)
    db.session.commit()

    return employee


def list_employees(search='', job_position=None, sort_by='name', direction='asc', page=1):
    query = Employee.query

    if search:
        query = query.filter(
            (Employee.name.ilike(f'%{search}%')) |
            (Employee.surname.ilike(f'%{search}%')) |
            (Employee.dni.ilike(f'%{search}%')) |
            (Employee.email.ilike(f'%{search}%'))
        )
    if job_position:
        query = query.filter(Employee.job_position == job_position)
    else:
        query = query  # No aplicar filtro, mostrar todos

    items_per_page = current_app.config.get('ITEMS_PER_PAGE')

    # Aplicar ordenación
    if sort_by in ['name', 'surname', 'start_date']:
        if direction == 'asc':
            query = query.order_by(getattr(Employee, sort_by).asc())
        else:
            query = query.order_by(getattr(Employee, sort_by).desc())

    pagination_employees = query.paginate(
        page=page, per_page=items_per_page, error_out=False)

    return pagination_employees


def get_by_email(email):
    employee = Employee.query.filter(Employee.email == email).first()
    return employee


def find_employee_by_name(name):
    employee = Employee.query.filter(Employee.name == name).first()
    return employee


def find_employee_by_apellido(surname):
    employee = Employee.query.filter(Employee.surname == surname).first()
    return employee


def find_employee_by_dni(dni):
    employee = Employee.query.filter(Employee.dni == dni).first()
    return employee


def find_employee_by_profession(profession):
    employee = Employee.query.filter(Employee.profession == profession).first()
    return employee


def update_employee(id, **kwargs):
    employee = Employee.query.filter(Employee.id == id).first()
    if not employee:
        return False
    for key, value in kwargs.items():
        setattr(employee, key, value)
    db.session.commit()
    return True


def delete_employee(id):
    employee = Employee.query.filter(Employee.id == id).first()
    if employee:
        if employee.documents:
            for document in employee.documents:
                document_repository.delete_document(document.id)
        db.session.delete(employee)
        db.session.commit()
        return True
    return False


def get_employees_by_job_positions(job_positions):
    if isinstance(job_positions, str):
        job_positions = [job_positions]
    return db.session.query(Employee).filter(Employee.job_position.in_(job_positions)).all()


def get_employee(id):
    employee = Employee.query.filter(Employee.id == id).first()
    return employee


def find_employee_by_associate_number(associate_number):
    employee = Employee.query.filter(
        Employee.associate_number == associate_number).first()
    return employee

def get_all():
    return Employee.query.all()
