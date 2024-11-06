from sqlalchemy import JSON
from src.core.database import db
from datetime import datetime

class Content(db.Model):
    __tablename__ = 'contents'
    
    id = db.Column(db.Integer, primary_key=True)
    publication_date = db.Column(db.DateTime, nullable=True)
    creation_date = db.Column(db.DateTime, nullable=False, default=datetime.now)
    update_date = db.Column(db.DateTime, nullable=False, default=datetime.now, onupdate=datetime.now)
    title = db.Column(db.String(255), nullable=False)
    summary = db.Column(db.String(255), nullable=False)
    content = db.Column(db.Text, nullable=False)
    status = db.Column(db.Enum('Borrador', 'Publicado', 'Archivado', name="status"), nullable=False, default='Borrador')

    author_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    author = db.relationship('User', backref='contents', uselist=False)  

    def __repr__(self):
        return f'<Content {self.title}>'

    def to_dict(self):
        return {
            'id': self.id,
        }
    
    def publish(self):
        self.publication_date = datetime.now()
        self.status = 'Publicado'

    def archive(self):
        self.status = 'Archivado'