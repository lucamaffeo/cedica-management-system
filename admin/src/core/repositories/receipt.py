from datetime import datetime, timedelta

from flask import flash, request
from src.core.database import db
from src.core.models.receipt import Receipt


def list_receipts(start_date=None, end_date=None, medio_pago=None, sort_by='id', direction='asc', page=1, items_per_page=5):
    # Iniciar la consulta
    query = Receipt.query

     # Obtener las fechas del formulario
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    
    

    # Filtrar por fecha si se proporcionan las fechas de inicio y fin
    if start_date and end_date :
        if start_date > end_date:
            flash("La fecha de inicio no puede ser mayor a la fecha de fin", "error")
        else:
            end_date = datetime.strptime(end_date, '%Y-%m-%d')  # Convertir str a fecha para poder agregar timedelta
            query = query.filter(Receipt.fecha_pago >= start_date, Receipt.fecha_pago < end_date + timedelta(days=1))
       
    # Filtrar por medio de pago si se proporciona
    if medio_pago:
        query = query.filter(Receipt.medio_pago == medio_pago)

    # Ordenar
    if direction == 'asc':
        query = query.order_by(getattr(Receipt, sort_by).asc())
    else:
        query = query.order_by(getattr(Receipt, sort_by).desc())

    paginated_receipts = query.paginate(page=page, per_page=items_per_page, error_out=False)

    return paginated_receipts

def create_receipt(**kwargs):
    receipt = Receipt(**kwargs)
    db.session.add(receipt)
    db.session.commit()
    return receipt

def update_receipt(id, **kwargs):
    receipt = Receipt.query.filter(Receipt.id == id).first()
    if not receipt:
        raise ValueError('Recibo no encontrado.')

    for key, value in kwargs.items():
        setattr(receipt, key, value)

    db.session.commit()
    return receipt

def delete_receipt(id):
    receipt = Receipt.query.filter(Receipt.id == id).first()
    if not receipt:
        raise ValueError('Recibo no encontrado.')
    
    db.session.delete(receipt)
    db.session.commit()

def get_receipt(id) -> Receipt | None:
    receipt = Receipt.query.filter(Receipt.id == id).first()
    return receipt
