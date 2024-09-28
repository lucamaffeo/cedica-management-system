from datetime import datetime
from src.core.database import db


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    password = db.Column(db.String(255), nullable=False)
    alias = db.Column(db.String(255), nullable=True)
    active = db.Column(db.Boolean, default=True)
    email = db.Column(db.String(255), nullable=False, unique=True)
    inserted_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'), nullable=False)
    role = db.relationship('Role', backref='user_role', lazy=True)

    def __repr__(self):
        return f"<User {self.email}>"

    def has_permission(self, permission: str):
        return any(permission == p.name for p in self.role.permissions)

    def to_dict(self):
        return {
            "id": self.id,
            "email": self.email,
            "alias": self.alias,
            "role": self.role_id,
            "active": self.active,
            "inserted_at": self.inserted_at,
            "updated_at": self.updated_at
        }
