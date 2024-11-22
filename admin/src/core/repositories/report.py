from flask import current_app
from src.core.models.rider import Rider
from src.core.database import db
from src.core.models.receipt import Receipt
from src.core.models.employee import Employee
from sqlalchemy import func, cast, String


def list_employees_by_seniority(sort_by='start_date', direction='asc', search=None, job_position=None, min_seniority=None, max_seniority=None, start_date=None, page=1, per_page=None):
    query = Employee.query

    # Filtros de búsqueda
    if search:
        query = query.filter(
            (Employee.name.ilike(f'%{search}%')) |
            (Employee.surname.ilike(f'%{search}%')) |
            (Employee.job_position.ilike(f'%{search}%'))
        )

    if job_position:
        query = query.filter(Employee.job_position.ilike(f'%{job_position}%'))

    if min_seniority is not None:
        query = query.filter(func.date_part(
            'year', func.age(Employee.start_date)) >= min_seniority)
    if max_seniority is not None:
        query = query.filter(func.date_part(
            'year', func.age(Employee.start_date)) <= max_seniority)

    # Filtro de fecha de ingreso
    if start_date:
        query = query.filter(Employee.start_date >= start_date)

    # Ordenar
    if sort_by == 'start_date':
        query = query.order_by(Employee.start_date.asc(
        ) if direction == 'asc' else Employee.start_date.desc())

    # Paginación
    items_per_page = current_app.config.get('ITEMS_PER_PAGE')
    pagination = query.paginate(
        page=page, per_page=items_per_page, error_out=False)

    return pagination


def list_receipts_by_payment_method(payment_method=None, start_date=None, end_date=None,
                                    sort_by='payment_method', direction='asc',
                                    min_receipts=None, max_receipts=None,
                                    min_quantity=None, max_quantity=None, page=1, per_page=10):
    query = db.session.query(
        Receipt.payment_method,
        func.sum(Receipt.quantity).label('total_quantity'),
        func.count(Receipt.id).label('total_receipts')
    ).group_by(Receipt.payment_method)

    # Filtro por método de pago (convertimos el Enum a String)
    if payment_method:
        query = query.filter(
            cast(Receipt.payment_method, String).ilike(f"%{payment_method}%"))

    # Filtros de fecha
    if start_date:
        query = query.filter(Receipt.payment_date >= start_date)
    if end_date:
        query = query.filter(Receipt.payment_date <= end_date)

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
    if sort_by and hasattr(Receipt, sort_by):
        column = getattr(Receipt, sort_by)
        if direction == 'desc':
            query = query.order_by(column.desc())
        else:
            query = query.order_by(column.asc())

    # Paginación
    items_per_page = current_app.config.get(
        'ITEMS_PER_PAGE', per_page)  # Por defecto 10 items por página
    pagination = query.paginate(
        page=page, per_page=items_per_page, error_out=False)

    return pagination


def list_riders_by_age(sort_by='age', direction='asc', name=None, surname=None, dni=None, min_age=None, max_age=None, page=1, per_page=10):
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
    if sort_by == 'age':
        if direction == 'asc':
            query = query.order_by(Rider.age.asc())
        else:
            query = query.order_by(Rider.age.desc())

    # Paginación
    items_per_page = current_app.config.get('ITEMS_PER_PAGE', per_page)
    pagination = query.paginate(
        page=page, per_page=items_per_page, error_out=False)

    return pagination
