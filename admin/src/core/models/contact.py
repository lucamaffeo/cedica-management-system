from datetime import datetime
from src.core.database import db

class ContactStatus(db.Model):
    __tablename__ = 'contact_statuses'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), unique=True, nullable=False)

class Contact(db.Model):
    __tablename__ = 'contacts'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=False)
    comment = db.Column(db.Text, nullable=True)
    inserted_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)
    updated_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)

    status_id = db.Column(db.Integer, db.ForeignKey('contact_statuses.id'), nullable=False, default=1)
    status = db.relationship('ContactStatus', backref='contacts_status', lazy=True)

    @property
    def formatted_inserted_at(self):
        return self.inserted_at.strftime('%Y-%m-%d %H:%M')

    @property
    def formated_updated_at(self):
        return self.updated_at.strftime('%Y-%m-%d %H:%M')

    def __repr__(self):
        return f"<Contact #{self.id} by {self.email}>"

    def to_dict(self):
        return {
                "id": self.id,
                "email": self.email,
                "body": self.description,
                "status": self.status.name,
                "comment": self.comment,
                "inserted_at": self.inserted_at,
                "updated_at": self.updated_at
                }
