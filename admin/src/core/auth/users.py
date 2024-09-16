from datetime import datetime
from src.core.database import db


class User(db.Model):
    tablename = 'users'

    id = db.column(db.Integer, primary_key=True)
    password = db.column(db.String(255), nullable=False)
    email = db.column(db.String(255), nullable=False)
    inserted_at = db.column(db.DateTime, default=datetime.now)
    updated_at = db.column(db.DateTime, default=datetime.now, onupdate=datetime.now)

def repr(self):
    return f"<User {self.username}>"

