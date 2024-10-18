from sqlalchemy import JSON
from src.core.database import db

class Tutor(db.Model):
    __tablename__ = 'tutors'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    surname = db.Column(db.String(100), nullable=False)
    dni = db.Column(db.String(20), unique=True, nullable=False)
    address = db.Column(db.String(255))
    cellphone = db.Column(db.String(50))
    email = db.Column(db.String(120), unique=True, nullable=False)
    educational_level = db.Column(db.Enum('Primario', 'Secundario', 'Terciario', 'Universitario', name='educational_level'))
    occupation = db.Column(db.String(100))

    def __repr__(self):
        return f'<Tutor {self.name} {self.surname}>'
