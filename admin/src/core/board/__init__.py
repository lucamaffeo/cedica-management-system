from src.core.database import db
from src.core.board.horse import Horse
from src.core.board.receipt import Receipt
from src.core.board.jinetesAmazona import JineteAmazonas
from src.core.board.payment import Payment

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

def list_JineteAmazonas():
    jinetesAmazonas = JineteAmazonas.query.all()
    return jinetesAmazonas

def create_jineteAmazona(**kwargs):
    jineteAmazona = JineteAmazonas(**kwargs)
    db.session.add(jineteAmazona)
    db.session.commit()

    return jineteAmazona

def create_payment(**kwargs):
    payment = Payment(**kwargs)
    db.session.add(payment)
    db.session.commit()

    return payment

def list_payments():
    payments = Payment.query.all()
    return payments