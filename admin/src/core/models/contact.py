from datetime import datetime
from src.core.database import db

class Contact(db.Model):
    __tablename__ = 'contacts'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=False)
    body = db.Column(db.Text, nullable=False)
    status = db.Column(db.String(50), default='pending')
    comment = db.Column(db.Text, nullable=True)
    inserted_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)

    @property
    def formatted_inserted_at(self):
        return self.inserted_at.strftime('%Y-%m-%d %H:%M')

    def __repr__(self):
        return f"<Contact {self.email}>"

    def to_dict(self):
        return {
            "id": self.id,
            "fullname": self.name,
            "email": self.email,
            "body": self.body,
            "status": self.status,
            "comment": self.comment,
            "inserted_at": self.inserted_at,
            "updated_at": self.updated_at
        }
