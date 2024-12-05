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
    title = db.Column(db.String(50), nullable=False)
    document_type = db.Column(db.Enum('Entrevista', 'Evaluación', 'Planificaciones', 'Evolución', 'Crónicas', 'Documental',
                                      'Ficha general del caballo', 'Planificación de Entrenamiento',
                                      'Informe de Evolución', 'Carga de Imágenes', 'Registro veterinario',
                                      'Otro',
                                      name='document_type'))

    upload_date = db.Column(db.DateTime, default=datetime.now)
    entity_id = db.Column(db.Integer, nullable=False)
    entity_type = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        return f"<Document {self.title}>"