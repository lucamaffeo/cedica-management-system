from datetime import datetime, timedelta
from src.core.database import db
from src.core.models.receipt import Receipt
from src.core.repositories import employee

def list_receipts(start_date=None, end_date=None, medio_pago=None, sort_by='id', direction='asc', page=1, items_per_page=5):
    # Iniciar la consulta
    query = Receipt.query

    # Filtrar por fecha si se proporcionan las fechas de inicio y fin
    if start_date and end_date:
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
    # Validar si los campos requeridos están presentes
    # if kwargs.get('type') == 'Administracion':
    #     if not kwargs.get('empleado_id'):
    #         raise ValueError('Empleado ID es requerido.')
    #     else:
    #         administracion = employee.get_employee(kwargs.get('empleado_id'))
    #         if not administracion:
    #             raise ValueError('Administracion ID no existe')
    # else:
    #     kwargs['empleado_id'] = None        

    receipt = Receipt(**kwargs)
    db.session.add(receipt)
    db.session.commit()
    return receipt

def update_receipt(id, **kwargs):
    receipt = Receipt.query.filter(Receipt.id == id).first()
    if not receipt:
        raise ValueError('Recibo no encontrado.')

    # Check the type and administracion_id for validation
    # new_type = kwargs.get('type')
    # if new_type == 'Administracion':
    #         if not kwargs.get('empleado_id'):
    #             raise ValueError('Empleado ID is required when the type is Administracion.')
    #         else:
    #             beneficiary = employee.get_employee(kwargs.get('empleado_id'))
    #             if not beneficiary:
    #                 raise ValueError('Empleado ID does not exist.')
    # else:
    #     kwargs['empleado_id'] = None

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

