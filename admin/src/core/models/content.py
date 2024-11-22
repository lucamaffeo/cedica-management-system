from sqlalchemy import JSON
from src.core.database import db
from datetime import datetime


class ContentStatus(db.Model):
    __tablename__ = 'content_statuses'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), unique=True, nullable=False)


class Content(db.Model):
    __tablename__ = 'contents'

    id = db.Column(db.Integer, primary_key=True)
    publication_date = db.Column(db.DateTime, nullable=True)
    creation_date = db.Column(
        db.DateTime, nullable=False, default=datetime.now)
    update_date = db.Column(db.DateTime, nullable=True,
                            default=datetime.now, onupdate=datetime.now)
    title = db.Column(db.String(255), nullable=False)
    summary = db.Column(db.Text, nullable=False)
    content = db.Column(db.Text, nullable=False)
    status_id = db.Column(db.Integer, db.ForeignKey(
        'content_statuses.id'), nullable=False, default=1)
    status = db.relationship(
        'ContentStatus', backref='contents_status', lazy=True)

    author_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    author = db.relationship('User', backref='contents', uselist=False)

    def __repr__(self):
        return f'<Content {self.title}>'

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'creation_date': self.creation_date,
            'publication_date': self.publication_date,
            'update_date': self.update_date,
            'status': self.status.name,
            'author': self.author.name if self.author else None
        }
