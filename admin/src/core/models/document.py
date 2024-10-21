from src.core.database import db
from datetime import datetime

class Document(db.Model):
    __tablename__ = 'documents'
    id = db.Column(db.Integer, primary_key=True)    
    file = db.Column(db.String(255))
    link = db.Column(db.String(255))
    title = db.Column(db.String(50), nullable=False)
    document_type = db.Column(db.Enum('Entrevista', 'Evaluación', 'Planificaciones', 'Evolución', 'Crónicas', 'Documental', name='document_type'))
    upload_date = db.Column(db.DateTime, default=datetime.now, nullable=False)
    # Relación con Rider 
    rider_id = db.Column(db.Integer, db.ForeignKey('riders.id'), nullable=False)  
    rider = db.relationship('Rider', backref=db.backref('documents', lazy=True))
  

    def __repr__(self):
        return f"<Document {self.title}>"