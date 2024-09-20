from datetime import datetime
from src.core.database import db


class User(db.Model):
    __tablename__ = 'users'

    id = db.column(db.Integer, primary_key=True)
    password = db.column(db.String(255), nullable=False)
    email = db.column(db.String(255), nullable=False)
    issues = db.relationship('Issue', back_populates='user')
    inserted_at = db.column(db.DateTime, default=datetime.now)
    updated_at = db.column(db.DateTime, default=datetime.now, onupdate=datetime.now)

def repr(self):
    return f"<User {self.username}>"

