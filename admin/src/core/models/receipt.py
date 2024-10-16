from datetime import datetime
from sqlalchemy import JSON
from src.core.database import db

class Receipt(db.Model):
    __tablename__ = 'receipts'
    
    id = db.Column(db.Integer, primary_key=True)
    ja_id = db.Column(db.Integer, db.ForeignKey('riders.id'), nullable=False)
    fecha_pago = db.Column(db.DateTime, default=datetime.now, nullable=False)
    monto = db.Column(db.Numeric(10, 2), nullable=False)
    medio_pago = db.Column(db.Enum('Efectivo', 'Tarjeta de Crédito', 'Tarjeta de Débito', name='medio_pago'), nullable=False)
    empleado_id = db.Column(db.Integer, db.ForeignKey('employees.id', ondelete='CASCADE'), nullable=False)
    observaciones = db.Column(db.Text)
    al_dia = db.Column(db.Boolean, default=True)

    # Relaciones
    ja = db.relationship('Rider', backref='receipts')  # Relación con Jinetes y Amazonas (J&A)
    empleado = db.relationship('Employee', backref='receipts')  # Relación con Empleados
    
    def __repr__(self):
        return f'<Receipt {self.id} - {self.monto} - {"Al Día" if self.al_dia else "En Deuda"}>'
