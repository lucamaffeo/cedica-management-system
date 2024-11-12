from src.core.models.rider import Rider
from src.core.models.employee import Employee
from src.core.models.horse import Horse
from src.core.database import db
from datetime import datetime
from sqlalchemy.orm import relationship

class Document(db.Model):
    __tablename__ = 'documents'
    id = db.Column(db.Integer, primary_key=True)
    file = db.Column(db.String(255))
    title = db.Column(db.String(50), default='', nullable=False)
    document_type = db.Column(db.Enum('Entrevista', 'Evaluación', 'Planificaciones', 'Evolución', 'Crónicas', 'Documental', 
                                  'Ficha general del caballo', 'Planificación de Entrenamiento', 
                                  'Informe de Evolución', 'Carga de Imágenes', 'Registro veterinario', 
                                   'Otro',
                                  name='document_type'))
    
    upload_date = db.Column(db.DateTime, default=datetime.now)
    entity_id = db.Column(db.Integer, nullable=False)
    entity_type = db.Column(db.String(50), nullable=False)

    entity = relationship(
        "Rider",
        primaryjoin="and_(foreign(Document.entity_id) == Rider.id, Document.entity_type == 'riders')",
        backref="documents",
        uselist=False
    ) or relationship(
        "Employee",
        primaryjoin="and_(foreign(Document.entity_id) == Employee.id, Document.entity_type == 'employees')",
        backref="documents",
        uselist=False
    ) or relationship(
        "Horse",
        primaryjoin="and_(foreign(Document.entity_id) == Horse.id, Document.entity_type == 'horses')",
        backref="documents",
        uselist=False
    )

    def __repr__(self):
        return f"<Document {self.title}>"
