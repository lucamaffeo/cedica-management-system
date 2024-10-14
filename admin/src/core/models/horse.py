from datetime import datetime
from sqlalchemy import JSON
from src.core.database import db

class Horse(db.Model):
    __tablename__ = 'horses'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    birth_date = db.Column(db.DateTime)
    gender = db.Column(db.Enum('Macho', 'Hembra', name='gender'), nullable=False)
    breed = db.Column(db.String(50))
    coat = db.Column(db.String(50))
    purchase_donation = db.Column(db.Enum('Compra', 'Donacion', name='purchase_donation'), nullable=False)
    entry_date = db.Column(db.DateTime, default=datetime.now)
    assigned_location = db.Column(db.String(100))
    trainer_id = db.Column(db.Integer, db.ForeignKey('employees.id', ondelete='CASCADE'))
    assigned_activities_ja = db.Column(db.Enum('Hipoterapia', 'Monta Terapéutica', 'Deporte Ecuestre Adaptado', 'Actividades Recreativas', 'Equitación', name='assigned_activities'))
    documentacion = db.Column(JSON)

    employee = db.relationship('Employee', backref='horses')

    def __repr__(self):
        return f'<Horse {self.name}>'
    

def has_permission(self, permission: str):
    return any(permission == p.name for p in self.role.permissions)
