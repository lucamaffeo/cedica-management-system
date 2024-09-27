from sqlalchemy import JSON
from src.core.database import db


class Employee(db.Model):
    __tablename__ = 'employees'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    surname = db.Column(db.String(100), nullable=False)
    dni = db.Column(db.String(20), unique=True, nullable=False)
    adress = db.Column(db.String(255))
    email = db.Column(db.String(120), unique=True, nullable=False)
    city = db.Column(db.String(100))
    telephone = db.Column(db.String(50))
    profession = db.Column(db.String(100))
    job_position = db.Column(db.String(100))
    start_date = db.Column(db.DateTime, nullable=False)
    termination_date = db.Column(db.DateTime, nullable=True)
    emergency_contact = db.Column(db.String(100))
    emergency_telephone = db.Column(db.String(50))
    social_work = db.Column(db.String(100))
    associate_number = db.Column(db.String(50))
    condition = db.Column(db.String(50))  # Voluntario o Personal Rentado
    active = db.Column(db.Boolean, default=True, nullable=False)
    documentation = db.Column(JSON)
    
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    user = db.relationship('User', backref='employee', uselist=False)

    def __repr__(self):
        return f'<Employee {self.name} {self.surname}>'
