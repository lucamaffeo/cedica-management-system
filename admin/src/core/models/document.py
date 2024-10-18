from src.core.database import db
from datetime import datetime

rider_assignment = db.Table(
        'document_action',
        db.Column('document_id', db.Integer, db.ForeignKey('documents.id'), primary_key=True),
        db.Column('action_id', db.Integer, db.ForeignKey('actions.id'), primary_key=True)
        )

class Document(db.Model):
    __tablename__ = 'documents'
    id = db.Column(db.Integer, primary_key=True)    
    file = db.Column(db.String(255))
    link = db.Column(db.String(255))
    title = db.Column(db.String(50), nullable=False)
    document_type = db.Column(db.Enum('Entrevista', 'Evaluación', 'Planificaciones', 'Evolución', 'Crónicas', 'Documental', name='document_type'))
    upload_date = db.Column(db.DateTime, default=datetime.now, nullable=False)
    actions = db.relationship('Action', secondary='document_action', backref='documents')

    def __repr__(self):
        return f"<Document {self.title}>"