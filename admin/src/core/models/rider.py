from datetime import datetime
from src.core.database import db

rider_assignment = db.Table(
        'rider_assignment',
        db.Column('rider_id', db.Integer, db.ForeignKey('riders.id'), primary_key=True),
        db.Column('assignment_id', db.Integer, db.ForeignKey('assignments.id'), primary_key=True)
        )

rider_tutor = db.Table(
        'rider_tutor',
        db.Column('rider_id', db.Integer, db.ForeignKey('riders.id'), primary_key=True),
        db.Column('tutor_id', db.Integer, db.ForeignKey('tutors.id'), primary_key=True),
        db.Column('relationship', db.String(50))
        )

rider_day = db.Table(
        'rider_day',
        db.Column('rider_id', db.Integer, db.ForeignKey('riders.id'), primary_key=True),
        db.Column('day_id', db.Integer, db.ForeignKey('days.id'), primary_key=True)
        )

rider_document = db.Table(
        'rider_document',
        db.Column('rider_id', db.Integer, db.ForeignKey('riders.id'), primary_key=True),
        db.Column('document_id', db.Integer, db.ForeignKey('documents.id'), primary_key=True)
        )

class Rider(db.Model):
    __tablename__ = 'riders'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    surname = db.Column(db.String(100), nullable=False)
    dni = db.Column(db.String(20), unique=True, nullable=False)
    age = db.Column(db.Integer, nullable=False)
    birthdate = db.Column(db.DateTime, nullable=False)
    birth_place = db.Column(db.String(100), nullable=False)
    address = db.Column(db.String(255), nullable=False)
    phone = db.Column(db.String(50), nullable=False)
    emergency_contact = db.Column(db.String(100))
    emergency_contact_phone_number = db.Column(db.String(50))
    scholarship = db.Column(db.Boolean, default=False)
    scholarship_percentage = db.Column(db.Numeric(5, 2))
    professionals = db.Column(db.Text)  # Campo libre para listar los profesionales
    disability_certificate = db.Column(db.Boolean, default=False)
    diagnosis = db.Column(db.Enum('ECNE', 'Lesión post-traumática', 'Mielomeningocele', 'Esclerosis Múltiple', 'Escoliosis Leve', 'Secuelas de ACV', 'Discapacidad Intelectual', 'Trastorno del Espectro Autista', 'Trastorno del Aprendizaje', 'Trastorno por Déficit de Atención/Hiperactividad',     'Trastorno de la Comunicación', 'Trastorno de Ansiedad', 'Síndrome de Down', 'Retraso Madurativo', 'Psicosis', 'Trastorno de Conducta', 'Trastornos del ánimo y afectivos', 'Trastorno Alimentario', 'OTRO', name='diagnosis'))
    other = db.Column(db.String(100), default=None)
    disability_type = db.Column(db.Enum('Mental', 'Motora', 'Sensorial', 'Viceral', name='disability_type'))
    family_assignment = db.Column(db.Boolean)
    assignments = db.relationship('Assignment', secondary='rider_assignment', backref='riders')
    pension = db.Column(db.Enum('Provincial', 'Nacional', name='pension'), default=None)
    health_insurance = db.Column(db.String(100))
    affiliate_number = db.Column(db.String(30))
    guardianship = db.Column(db.Boolean)
    observations = db.Column(db.Text)
    school_institution = db.Column(db.String(100))
    institution_address = db.Column(db.String(255))
    grade = db.Column(db.String(100))
    institution_phone = db.Column(db.String(50))
    institution_observations = db.Column(db.Text)
    tutors = db.relationship('Tutor', secondary='rider_tutor', backref='riders')
    work_proposal = db.Column(db.Enum('Hipoterapia', 'Monta Terapéutica', 'Deporte Ecuestre Adaptado', 'Actividades Recreativas', 'Equitación', name='work_proposal'))
    condition = db.Column(db.Enum('Regular', 'De Baja', name='condition'))
    headquarters = db.Column(db.Enum('CASJ', 'HLP', 'OTRO', name='headquarters'))
    days = db.relationship('Day', secondary='rider_day', backref='riders')
    therapist_teacher_id = db.Column(db.Integer, db.ForeignKey('employees.id', ondelete='CASCADE'))
    horse_conductor_id = db.Column(db.Integer, db.ForeignKey('employees.id', ondelete='CASCADE'))
    horse_id = db.Column(db.Integer, db.ForeignKey('horses.id', ondelete='CASCADE'))
    track_assistant_id = db.Column(db.Integer, db.ForeignKey('employees.id', ondelete='CASCADE'))
    therapist_teacher = db.relationship('Employee', foreign_keys=[therapist_teacher_id], backref='riders_therapist_teacher')
    horse_conductor = db.relationship('Employee', foreign_keys=[horse_conductor_id], backref='riders_horse_conductor')
    horse = db.relationship('Horse', backref='riders')
    track_assistant = db.relationship('Employee', foreign_keys=[track_assistant_id], backref='riders_track_assistant')
    documents = db.relationship('Document', secondary='rider_document', backref='riders')

    def __repr__(self):
        return f'<Jinete/Amazona {self.name} {self.surname}>'
