from datetime import datetime
from src.core.database import db

class Payment(db.Model):
    __tablename__ = 'payment'
    
    id = db.Column(db.Integer, primary_key=True)
    beneficiario_id = db.Column(db.Integer, db.ForeignKey('employees.id'), nullable=False)
    monto = db.Column(db.Numeric(10, 2), nullable=False)
    fecha_pago = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    tipo_pago = db.Column(db.Enum('Honorarios', 'Proveedor', 'Gastos Varios', name='tipo_pago'), nullable=False)
    descripcion = db.Column(db.Text)

    def __repr__(self):
        return f'<Payment {self.id} - {self.monto}>'
