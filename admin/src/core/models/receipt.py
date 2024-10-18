from datetime import datetime
from sqlalchemy import JSON
from src.core.database import db

class Receipt(db.Model):
    __tablename__ = 'receipts'
    
    id = db.Column(db.Integer, primary_key=True)
    ja_id = db.Column(db.Integer, db.ForeignKey('riders.id'), nullable=False)
    payment_date = db.Column(db.DateTime, default=datetime.now, nullable=False)
    quantity = db.Column(db.Numeric(10, 2), nullable=False)
    payment_method = db.Column(db.Enum('Efectivo', 'Tarjeta de Crédito', 'Tarjeta de Débito', 'Transferencia', 'Otro', name='payment_method'), nullable=False)
    employee_id = db.Column(db.Integer, db.ForeignKey('employees.id', ondelete='CASCADE'), nullable=False)
    remarks = db.Column(db.Text)
    up_to_date = db.Column(db.Boolean, default=True)

    # Relaciones
    ja = db.relationship('Rider', backref='receipts')  # Relación con Jinetes y Amazonas (J&A)
    employee = db.relationship('Employee', backref='receipts')  # Relación con Empleados
    
    def __repr__(self):
        return f'<Receipt {self.id} - {self.quantity} - {"Al Día" if self.up_to_date else "En Deuda"}>'
