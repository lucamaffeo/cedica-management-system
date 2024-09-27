from datetime import datetime
from sqlalchemy import JSON
from src.core.database import db

class JineteAmazonas(db.Model):
    __tablename__ = 'jinetes_amazonas'
    
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    apellido = db.Column(db.String(100), nullable=False)
    dni = db.Column(db.String(20), unique=True, nullable=False)
    edad = db.Column(db.Integer)
    fecha_nacimiento = db.Column(db.DateTime)
    lugar_nacimiento = db.Column(db.String(100))
    domicilio = db.Column(db.String(255))
    telefono = db.Column(db.String(50))
    contacto_emergencia = db.Column(db.String(100))
    tel_contacto = db.Column(db.String(50))
    becado = db.Column(db.Boolean, default=False)
    porcentaje_beca = db.Column(db.Numeric(5, 2))
    profesionales = db.Column(db.Text)  # Campo libre para listar los profesionales
    documentacion = db.Column(JSON)

    def __repr__(self):
        return f'<Jinete/Amazona {self.nombre} {self.apellido}>'