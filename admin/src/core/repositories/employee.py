from flask import current_app
from src.core.database import db
from src.core.models.employee import Employee
from src.core.repositories import document as document_repository


def create_employee(**kwargs):
    """
    Crea un nuevo empleado y lo agrega a la base de datos.

    Args:
        **kwargs: Argumentos de palabra clave para los atributos del empleado.

    Returns:
        Employee: El objeto empleado creado.
    """
    employee = Employee(**kwargs)
    db.session.add(employee)
    db.session.commit()

    return employee


def list_employees(search='', job_position=None, sort_by='name', direction='asc', page=1):
    """
    Lista empleados con búsqueda, filtro y ordenación opcionales.

    Args:
        search (str): Término de búsqueda para los atributos del empleado.
        job_position (str): Posición de trabajo para filtrar empleados.
        sort_by (str): Atributo por el cual ordenar.
        direction (str): Dirección de ordenación ('asc' o 'desc').
        page (int): Número de página para la paginación.

    Returns:
        Pagination: Lista paginada de empleados.
    """
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
    """
    Recupera un empleado por correo electrónico.

    Args:
        email (str): El correo electrónico del empleado.

    Returns:
        Employee: El objeto empleado o None si no se encuentra.
    """
    employee = Employee.query.filter(Employee.email == email).first()
    return employee


def find_employee_by_name(name):
    """
    Encuentra un empleado por nombre.

    Args:
        name (str): El nombre del empleado.

    Returns:
        Employee: El objeto empleado o None si no se encuentra.
    """
    employee = Employee.query.filter(Employee.name == name).first()
    return employee


def find_employee_by_apellido(surname):
    """
    Encuentra un empleado por apellido.

    Args:
        surname (str): El apellido del empleado.

    Returns:
        Employee: El objeto empleado o None si no se encuentra.
    """
    employee = Employee.query.filter(Employee.surname == surname).first()
    return employee


def find_employee_by_dni(dni):
    """
    Encuentra un empleado por DNI.

    Args:
        dni (str): El DNI del empleado.

    Returns:
        Employee: El objeto empleado o None si no se encuentra.
    """
    employee = Employee.query.filter(Employee.dni == dni).first()
    return employee


def find_employee_by_profession(profession):
    """
    Encuentra un empleado por profesión.

    Args:
        profession (str): La profesión del empleado.

    Returns:
        Employee: El objeto empleado o None si no se encuentra.
    """
    employee = Employee.query.filter(Employee.profession == profession).first()
    return employee


def update_employee(id, **kwargs):
    """
    Actualiza los atributos de un empleado.

    Args:
        id (int): El ID del empleado.
        **kwargs: Argumentos de palabra clave para los atributos del empleado.

    Returns:
        bool: True si la actualización fue exitosa, False en caso contrario.
    """
    employee = Employee.query.filter(Employee.id == id).first()
    if not employee:
        return False
    for key, value in kwargs.items():
        setattr(employee, key, value)
    db.session.commit()
    return True


def delete_employee(id):
    """
    Elimina un empleado por ID.

    Args:
        id (int): El ID del empleado.

    Returns:
        bool: True si la eliminación fue exitosa, False en caso contrario.
    """
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
    """
    Recupera empleados por posiciones de trabajo.

    Args:
        job_positions (list o str): Lista de posiciones de trabajo o una sola posición de trabajo.

    Returns:
        list: Lista de empleados que coinciden con las posiciones de trabajo.
    """
    if isinstance(job_positions, str):
        job_positions = [job_positions]
    return db.session.query(Employee).filter(Employee.job_position.in_(job_positions)).all()


def get_employee(id):
    """
    Recupera un empleado por ID.

    Args:
        id (int): El ID del empleado.

    Returns:
        Employee: El objeto empleado o None si no se encuentra.
    """
    employee = Employee.query.filter(Employee.id == id).first()
    return employee


def find_employee_by_associate_number(associate_number):
    """
    Encuentra un empleado por número de asociado.

    Args:
        associate_number (str): El número de asociado del empleado.

    Returns:
        Employee: El objeto empleado o None si no se encuentra.
    """
    employee = Employee.query.filter(
        Employee.associate_number == associate_number).first()
    return employee

def get_all():
    """
    Recupera todos los empleados.

    Returns:
        list: Lista de todos los empleados.
    """
    return Employee.query.all()
