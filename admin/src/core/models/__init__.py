from src.core.database import db
from src.core.models.receipt import Receipt
from src.core.models.rider import Rider
from src.core.models.payment import Payment


def list_riders():
    rider = Rider.query.all()
    return rider

def create_rider(**kwargs):
    rider = Rider(**kwargs)
    db.session.add(rider)
    db.session.commit()

    return rider

def create_payment(**kwargs):
    payment = Payment(**kwargs)
    db.session.add(payment)
    db.session.commit()

    return payment

def list_payments():
    payments = Payment.query.all()
    return payments
