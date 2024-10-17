from datetime import datetime
from sqlalchemy import JSON
from src.core.database import db

employee_association = db.Table(
    'employee_association',
    db.Column('employee_id', db.Integer, db.ForeignKey('employees.id'), primary_key=True),
    db.Column('horse_id', db.Integer, db.ForeignKey('horses.id'), primary_key=True)
    )

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
    assigned_activities_ja = db.Column(db.Enum('Hipoterapia', 'Monta Terapeutica', 'Deporte Ecuestre Adaptado', 'Actividades Recreativas', 'Equitación', name='assigned_activities'))
    documentacion = db.Column(JSON)
    association = db.relationship('Employee', secondary='employee_association', backref='horses', lazy='dynamic')
    

    def __repr__(self):
        return f'<Horse {self.name}>'
    

def has_permission(self, permission: str):
    return any(permission == p.name for p in self.role.permissions)
