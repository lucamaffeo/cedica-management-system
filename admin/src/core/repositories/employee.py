from src.core.database import db
from src.core.models.employee import Employee

def create_employee(**kwargs):
    employee = Employee(**kwargs)
    db.session.add(employee)
    db.session.commit()

    return employee

def list_employees(search='', profession=None, sort_by='name', direction='asc', page=1, items_per_page=5):
    query = Employee.query

    if search:
        query = query.filter(
            (Employee.name.ilike(f'%{search}%')) |
            (Employee.surname.ilike(f'%{search}%')) |
            (Employee.dni.ilike(f'%{search}%')) |
            (Employee.email.ilike(f'%{search}%'))
        )
    if profession is not None:
        query = query.filter(Employee.profession == profession)
    
    # Aplicar ordenación
    if sort_by in ['name', 'surname', 'start_date']:
        if direction == 'asc':
            query = query.order_by(getattr(Employee, sort_by).asc())
        else:
            query = query.order_by(getattr(Employee, sort_by).desc())
    

    paginated_users = query.paginate(page=page, per_page=items_per_page, error_out=False)

    return paginated_users

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

