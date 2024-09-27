from src.core.database import db
from src.core.models.horse import Horse
from src.core.models.receipt import Receipt
from src.core.models.rider import Rider
from src.core.models.payment import Payment

def list_Horse():
    horses = Horse.query.all()
    return horses

def list_Receipt():
    receipts = Receipt.query.all()
    return receipts 

def create_horse(**kwargs):
    horse = Horse(**kwargs)
    db.session.add(horse)
    db.session.commit()

    return horse

def create_receipt(**kwargs):
    receipt = Receipt(**kwargs)
    db.session.add(receipt)
    db.session.commit()

    return receipt

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
