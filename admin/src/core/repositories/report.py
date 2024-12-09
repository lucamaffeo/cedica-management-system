from flask import current_app
from src.core.models.rider import Rider
from src.core.database import db
from src.core.models.receipt import Receipt
from src.core.models.employee import Employee
from sqlalchemy import func, cast, String


def list_employees_by_seniority(sort_by='start_date', direction='asc', search=None, job_position=None, min_seniority=None, max_seniority=None, start_date=None, page=1, per_page=None):
    """
    Listar empleados por antigüedad con filtros y paginación.

    Args:
        sort_by (str): Campo por el cual ordenar.
        direction (str): Dirección de la ordenación ('asc' o 'desc').
        search (str): Cadena de búsqueda para filtrar por nombre, apellido o puesto de trabajo.
        job_position (str): Puesto de trabajo para filtrar.
        min_seniority (int): Antigüedad mínima en años.
        max_seniority (int): Antigüedad máxima en años.
        start_date (date): Fecha de inicio para filtrar.
        page (int): Número de página para la paginación.
        per_page (int): Número de elementos por página.

    Returns:
        Pagination: Objeto de paginación con los empleados.
    """
    query = Employee.query

    # Filtros de búsqueda
    if search:
        query = query.filter(
            (Employee.name.ilike(f'%{search}%')) |
            (Employee.surname.ilike(f'%{search}%')) 
        )

    if job_position:
        query = query.filter(Employee.job_position.ilike(f'%{job_position}%'))

     # Filtro de fecha de ingreso
    if start_date:
        query = query.filter(Employee.start_date == start_date)

    if min_seniority is not None:
        query = query.filter(func.date_part(
            'year', func.age(Employee.start_date)) >= min_seniority)
    if max_seniority is not None:
        query = query.filter(func.date_part(
            'year', func.age(Employee.start_date)) <= max_seniority)

    # Ordenar
    if sort_by in ['start_date', 'name', 'job_position']:
        column = getattr(Employee, sort_by)
        if direction == 'asc':
            query = query.order_by(column.asc())
        else:
            query = query.order_by(column.desc())

    if sort_by == 'seniority':
        if direction == 'asc':
            query = query.order_by(func.age(Employee.start_date).asc())
        else:
            query = query.order_by(func.age(Employee.start_date).desc())

    # Paginación
    items_per_page = current_app.config.get('ITEMS_PER_PAGE')
    pagination = query.paginate(
        page=page, per_page=items_per_page, error_out=False)

    return pagination


def list_receipts_by_payment_method(payment_method=None, start_date=None, end_date=None,
                                    sort_by='payment_method', direction='asc',
                                    min_receipts=None, max_receipts=None,
                                    min_quantity=None, max_quantity=None, page=1, per_page=10):
    """
    Listar recibos por método de pago con filtros y paginación.

    Args:
        payment_method (str): Método de pago para filtrar.
        start_date (date): Fecha de inicio para filtrar.
        end_date (date): Fecha de fin para filtrar.
        sort_by (str): Campo por el cual ordenar.
        direction (str): Dirección de la ordenación ('asc' o 'desc').
        min_receipts (int): Número mínimo de recibos.
        max_receipts (int): Número máximo de recibos.
        min_quantity (float): Cantidad mínima.
        max_quantity (float): Cantidad máxima.
        page (int): Número de página para la paginación.
        per_page (int): Número de elementos por página.

    Returns:
        Pagination: Objeto de paginación con los recibos.
    """
    query = db.session.query(
        Receipt.payment_method,
        func.sum(Receipt.quantity).label('total_quantity'),
        func.count(Receipt.id).label('total_receipts')
    ).group_by(Receipt.payment_method)

    # Filtro por método de pago (convertimos el Enum a String)
    if payment_method:
        query = query.filter(
            cast(Receipt.payment_method, String).ilike(f"%{payment_method}%"))

    # Filtros de recibos
    if min_receipts is not None:
        query = query.having(func.count(Receipt.id) >= min_receipts)
    if max_receipts is not None:
        query = query.having(func.count(Receipt.id) <= max_receipts)

    # Filtros de cantidad
    if min_quantity is not None:
        query = query.having(func.sum(Receipt.quantity) >= min_quantity)
    if max_quantity is not None:
        query = query.having(func.sum(Receipt.quantity) <= max_quantity)

    # Ordenar resultados
    if sort_by == 'payment_method':
        if direction == 'desc':
            query = query.order_by(Receipt.payment_method.desc())
        else:
            query = query.order_by(Receipt.payment_method.asc())
    
    if sort_by in ['total_quantity', 'total_receipts']:
        if direction == 'desc':
            query = query.order_by(func.count(Receipt.id).desc())
        else:
            query = query.order_by(func.count(Receipt.id).asc())

    # Paginación
    items_per_page = current_app.config.get(
        'ITEMS_PER_PAGE', per_page)  # Por defecto 10 items por página
    pagination = query.paginate(
        page=page, per_page=items_per_page, error_out=False)

    return pagination


def list_riders_by_age(sort_by='age', direction='asc', name=None, surname=None, dni=None, min_age=None, max_age=None, page=1, per_page=10):
    """
    Listar jinetes por edad con filtros y paginación.

    Args:
        sort_by (str): Campo por el cual ordenar.
        direction (str): Dirección de la ordenación ('asc' o 'desc').
        name (str): Nombre del jinete para filtrar.
        surname (str): Apellido del jinete para filtrar.
        dni (str): DNI del jinete para filtrar.
        min_age (int): Edad mínima.
        max_age (int): Edad máxima.
        page (int): Número de página para la paginación.
        per_page (int): Número de elementos por página.

    Returns:
        Pagination: Objeto de paginación con los jinetes.
    """
    query = Rider.query

    # Filtros por nombre, apellido, DNI y rango de edad
    if name:
        query = query.filter(Rider.name.ilike(
            f'%{name}%'))  # Filtro por nombre
    if surname:
        query = query.filter(Rider.surname.ilike(
            f'%{surname}%'))  # Filtro por apellido
    if dni:
        query = query.filter(Rider.dni.ilike(f'%{dni}%'))  # Filtro por DNI
    if min_age:
        query = query.filter(Rider.age >= min_age)  # Filtro por edad mínima
    if max_age:
        query = query.filter(Rider.age <= max_age)  # Filtro por edad máxima

    # Ordenar por edad
    if sort_by in ['age', 'name', 'surname','dni']:
        if direction == 'asc':
            query = query.order_by(getattr(Rider, sort_by).asc())
        else:
            query = query.order_by(getattr(Rider, sort_by).desc())
    # Paginación
    items_per_page = current_app.config.get('ITEMS_PER_PAGE', per_page)
    pagination = query.paginate(
        page=page, per_page=items_per_page, error_out=False)

    return pagination
