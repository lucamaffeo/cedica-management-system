from datetime import datetime
from src.core.database import db

class Payment(db.Model):
    __tablename__ = 'payments'
    
    id = db.Column(db.Integer, primary_key=True)
    beneficiary_id = db.Column(db.Integer, db.ForeignKey('employees.id', ondelete='CASCADE'), nullable=True)
    amount = db.Column(db.Numeric(10, 2), nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    type = db.Column(db.Enum('Honorarios', 'Proveedor', 'Gastos varios', name='tipo_pago'), nullable=False) #TODO change to string
    description = db.Column(db.Text)

    @property
    def formatted_date(self):
        return self.date.strftime('%Y-%m-%d %H:%M')

    def __repr__(self):
        return f'<Payment {self.id} - {self.amount}>'
