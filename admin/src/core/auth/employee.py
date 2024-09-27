from sqlalchemy import JSON
from src.core.database import db


class Employee(db.Model):
    __tablename__ = 'employees'
    
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    apellido = db.Column(db.String(100), nullable=False)
    dni = db.Column(db.String(20), unique=True, nullable=False)
    domicilio = db.Column(db.String(255))
    email = db.Column(db.String(120), unique=True, nullable=False)
    localidad = db.Column(db.String(100))
    telefono = db.Column(db.String(50))
    profesion = db.Column(db.String(100))
    puesto_laboral = db.Column(db.String(100))
    fecha_inicio = db.Column(db.DateTime, nullable=False)
    fecha_cese = db.Column(db.DateTime, nullable=True)
    contacto_emergencia = db.Column(db.String(100))
    telefono_emergencia = db.Column(db.String(50))
    obra_social = db.Column(db.String(100))
    n_afiliado = db.Column(db.String(50))
    condicion = db.Column(db.String(50))  # Voluntario o Personal Rentado
    activo = db.Column(db.Boolean, default=True, nullable=False)
    documentacion = db.Column(JSON)
    
    usuario_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    usuario = db.relationship('User', backref='employee', uselist=False)

    def __repr__(self):
        return f'<Employee {self.nombre} {self.apellido}>'
