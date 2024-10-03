from datetime import datetime
from sqlalchemy import JSON
from src.core.database import db

class Horse(db.Model):
    __tablename__ = 'horses'
    
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    fecha_nacimiento = db.Column(db.DateTime)
    sexo = db.Column(db.String(10))
    raza = db.Column(db.String(50))
    pelaje = db.Column(db.String(50))
    compra_donacion = db.Column(db.Enum('Compra', 'Donación', name='tipo_adquisicion'), nullable=False)
    fecha_ingreso = db.Column(db.DateTime, default=datetime.now)
    sede_asignada = db.Column(db.String(100))
    entrenador_id = db.Column(db.Integer, db.ForeignKey('employees.id', ondelete='CASCADE'))
    tipo_ja_asignados = db.Column(db.Enum('Hipoterapia', 'Monta Terapéutica', 'Deporte Ecuestre Adaptado', 'Actividades Recreativas', 'Equitación', name='tipo_ja')) # Jinetes y Amazonas
    documentacion = db.Column(JSON)

    def __repr__(self):
        return f'<Horse {self.nombre}>'