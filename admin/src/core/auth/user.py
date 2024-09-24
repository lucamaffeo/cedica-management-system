from datetime import datetime
from src.core.database import db


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    password = db.Column(db.String(255), nullable=False)    
    alias = db.Column(db.String(255), nullable=True)
    activo = db.Column(db.Boolean, default=True) #si/no
    email = db.Column(db.String(255), nullable=False, unique=True)
    inserted_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'), nullable=False)
    role = db.relationship('Role', backref='user_role')

def repr(self):
    return f"<User {self.alias}>"

