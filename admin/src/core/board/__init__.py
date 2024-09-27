from src.core.database import db
from src.core.board.payment import Payment

from sqlalchemy import text
from werkzeug.security import generate_password_hash

def create_payment(**kwargs):
    payment = Payment(**kwargs)
    db.session.add(payment)
    db.session.commit()

    return payment

def list_payments():
    payments = Payment.query.all()
    return payments