from datetime import timedelta

from flask import current_app, flash
from src.core.database import db
from src.core.models.payment import Payment
from src.core.repositories import employee
from datetime import datetime


def list_payments(start_date=None, end_date=None, payment_type=None, sort_by='alias', direction='asc', page=1):
    """
    Lista los pagos con filtros opcionales por fecha, tipo de pago y ordenamiento.

    :param start_date: Fecha de inicio para filtrar pagos.
    :param end_date: Fecha de fin para filtrar pagos.
    :param payment_type: Tipo de pago para filtrar.
    :param sort_by: Campo por el cual ordenar los resultados.
    :param direction: Dirección del ordenamiento ('asc' o 'desc').
    :param page: Número de página para la paginación.
    :return: Pagos paginados según los filtros aplicados.
    """

    query = Payment.query

    if start_date:
        try:
            start_date = datetime.strptime(start_date, '%Y-%m-%d')
            query = query.filter(Payment.date >= start_date)
        except ValueError:
            flash("La fecha de inicio es inválida.", "error")

    if end_date:
        try:
            end_date = datetime.strptime(
                end_date, '%Y-%m-%d') + timedelta(days=1)
            query = query.filter(Payment.date < end_date)
        except ValueError:
            flash("La fecha de fin es inválida.", "error")

    # Filter by payment type if provided
    if payment_type:
        query = query.filter(Payment.type == payment_type)

    # Order
    if direction == 'asc':
        query = query.order_by(getattr(Payment, sort_by).asc())
    else:
        query = query.order_by(getattr(Payment, sort_by).desc())

    items_per_page = current_app.config.get('ITEMS_PER_PAGE')

    paginated_payments = query.paginate(
        page=page, per_page=items_per_page, error_out=False)

    return paginated_payments


def get_payment_types():
    """
    Obtiene los tipos de pago disponibles.

    :return: Lista de tipos de pago.
    """
    return Payment.type.property.columns[0].type.enums


def create_payment(**kwargs):
    """
    Crea un nuevo pago en la base de datos.

    :param kwargs: Argumentos para crear un nuevo pago.
    :return: El pago creado.
    """
    # Check the type and beneficiary_id for validation
    if kwargs.get('type') == 'Honorarios':
        beneficiary = employee.get_employee(kwargs.get('beneficiary_id'))
        if not beneficiary:
            raise ValueError('Beneficiary ID does not exist.')
    else:
        kwargs['beneficiary_id'] = None

    payment = Payment(**kwargs)
    db.session.add(payment)
    db.session.commit()
    return payment


def update_payment(id, **kwargs):
    """
    Actualiza un pago existente en la base de datos.

    :param id: ID del pago a actualizar.
    :param kwargs: Argumentos para actualizar el pago.
    :return: El pago actualizado.
    """
    payment = Payment.query.filter(Payment.id == id).first()
    if not payment:
        raise ValueError('Payment not found.')

    # Check the type and beneficiary_id for validation
    new_type = kwargs.get('type')
    if new_type == 'Honorarios':
        beneficiary = employee.get_employee(kwargs.get('beneficiary_id'))
        if not beneficiary:
            raise ValueError('Beneficiary ID does not exist.')
    else:
        kwargs['beneficiary_id'] = None

    for key, value in kwargs.items():
        setattr(payment, key, value)
    db.session.commit()
    return payment


def delete_payment(id):
    """
    Elimina un pago de la base de datos.

    :param id: ID del pago a eliminar.
    :return: True si el pago fue eliminado, False si no se encontró.
    """
    payment = Payment.query.filter(Payment.id == id).first()
    if payment:
        db.session.delete(payment)
        db.session.commit()
        return True
    return False


def get_payment(id) -> Payment | None:
    """
    Obtiene un pago por su ID.

    :param id: ID del pago a obtener.
    :return: El pago si se encuentra, None si no.
    """
    payment = Payment.query.filter(Payment.id == id).first()
    return payment
