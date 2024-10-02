from datetime import datetime
from src.core.database import db

class Payment(db.Model):
    __tablename__ = 'payments'
    
    id = db.Column(db.Integer, primary_key=True)
    beneficiary_id = db.Column(db.Integer, db.ForeignKey('employees.id', ondelete='CASCADE'), nullable=False)
    amount = db.Column(db.Numeric(10, 2), nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    type = db.Column(db.Enum('Honorarios', 'Proveedor', 'Gastos Varios', name='tipo_pago'), nullable=False)
    description = db.Column(db.Text)

    def __repr__(self):
        return f'<Payment {self.id} - {self.amount}>'
