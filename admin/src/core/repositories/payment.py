from datetime import timedelta

from flask import current_app
from src.core.database import db
from src.core.models.payment import Payment
from src.core.repositories import employee
from datetime import datetime


def list_payments(start_date=None, end_date=None, payment_type=None, sort_by='alias', direction='asc', page=1):
    # Init db query
    query = Payment.query


    if start_date and end_date:
        end_date = datetime.strptime(end_date, '%Y-%m-%d')  # Convert str to date, so we can add timedelta (to make end_date include that day on results)
        query = query.filter(Payment.date >= start_date, Payment.date < end_date + timedelta(days=1))

    # Filter by payment type if provided
    if payment_type:
        query = query.filter(Payment.type == payment_type)

    # Order
    if direction == 'asc':
        query = query.order_by(getattr(Payment, sort_by).asc())
    else:
        query = query.order_by(getattr(Payment, sort_by).desc())

    items_per_page = current_app.config.get('ITEMS_PER_PAGE')

    paginated_payments = query.paginate(page=page, per_page=items_per_page, error_out=False)

    return paginated_payments

def get_payment_types():
    return Payment.type.property.columns[0].type.enums

def create_payment(**kwargs):
    # Check the type and beneficiary_id for validation
    if kwargs.get('type') == 'Honorarios':
        if not kwargs.get('beneficiary_id'):
            raise ValueError('Beneficiary ID is required when the type is Honorarios.')
        else:
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
    payment = Payment.query.filter(Payment.id == id).first()
    if not payment:
        raise ValueError('Payment not found.')

    # Check the type and beneficiary_id for validation
    new_type = kwargs.get('type')
    if new_type == 'Honorarios':
            if not kwargs.get('beneficiary_id'):
                raise ValueError('Beneficiary ID is required when the type is Honorarios.')
            else:
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
    payment = Payment.query.filter(Payment.id == id).first()
    if payment:
        db.session.delete(payment)
        db.session.commit()
        return True
    return False

def get_payment(id) -> Payment | None:
    payment = Payment.query.filter(Payment.id == id).first()
    return payment
