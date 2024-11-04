from datetime import datetime, timedelta

from flask import current_app, flash, request
from src.core.database import db
from src.core.models.receipt import Receipt


def list_receipts(start_date=None, end_date=None, payment_method=None, sort_by='id', direction='asc', page=1):
    # Iniciar la consulta
    query = Receipt.query

    # Obtener las fechas del formulario
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')

    # Filtrar por fecha de inicio, fin o ambas
    if start_date:
        try:
            start_date = datetime.strptime(start_date, '%Y-%m-%d')
            query = query.filter(Receipt.payment_date >= start_date)
        except ValueError:
            flash("La fecha de inicio es inválida.", "error")

    if end_date:
        try:
            end_date = datetime.strptime(end_date, '%Y-%m-%d') + timedelta(days=1)
            query = query.filter(Receipt.payment_date < end_date)
        except ValueError:
            flash("La fecha de fin es inválida.", "error")

    # Filtrar por medio de pago si se proporciona
    if payment_method:
        query = query.filter(Receipt.payment_method == payment_method)

    # Ordenar
    if direction == 'asc':
        query = query.order_by(getattr(Receipt, sort_by).asc())
    else:
        query = query.order_by(getattr(Receipt, sort_by).desc())

    # Paginación
    items_per_page = current_app.config.get('ITEMS_PER_PAGE')
    paginated_receipts = query.paginate(page=page, per_page=items_per_page, error_out=False)

    return paginated_receipts

def create_receipt(**kwargs):
    receipt = Receipt(**kwargs)
    db.session.add(receipt)
    db.session.commit()
    return receipt

def update_receipt(receipt: Receipt, **kwargs):
    for key, value in kwargs.items():
        setattr(receipt, key, value)
    db.session.commit()
    return receipt

def delete_receipt(receipt: Receipt):
    db.session.delete(receipt)
    db.session.commit()

def get_receipt(id) -> Receipt | None:
    receipt = Receipt.query.filter(Receipt.id == id).first()
    return receipt
