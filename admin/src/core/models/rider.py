from datetime import datetime
from sqlalchemy import JSON
from src.core.database import db

rider_assignment = db.Table(
        'rider_assignment',
        db.Column('rider_id', db.Integer, db.ForeignKey('rider.id'), primary_key=True),
        db.Column('assignment_id', db.Integer, db.ForeignKey('passignment.id'), primary_key=True)
        )

rider_tutor = db.Table(
        'rider_tutor',
        db.Column('rider_id', db.Integer, db.ForeignKey('rider.id'), primary_key=True),
        db.Column('tutor_id', db.Integer, db.ForeignKey('tutor.id'), primary_key=True),
        db.Column('relationship', db.String(50))
        )

rider_day = db.Table(
        'rider_day',
        db.Column('rider_id', db.Integer, db.ForeignKey('rider.id'), primary_key=True),
        db.Column('day_id', db.Integer, db.ForeignKey('day.id'), primary_key=True)
        )


class Rider(db.Model):
    __tablename__ = 'riders'
    
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    apellido = db.Column(db.String(100), nullable=False)
    dni = db.Column(db.String(20), unique=True, nullable=False)
    edad = db.Column(db.Integer)
    fecha_nacimiento = db.Column(db.DateTime)
    lugar_nacimiento = db.Column(db.String(100))
    domicilio = db.Column(db.String(255))
    telefono = db.Column(db.String(50))
    contacto_emergencia = db.Column(db.String(100))
    tel_contacto = db.Column(db.String(50))
    becado = db.Column(db.Boolean, default=False)
    porcentaje_beca = db.Column(db.Numeric(5, 2))
    profesionales = db.Column(db.Text)  # Campo libre para listar los profesionales
    certificado_discapacidad = db.Column(db.Boolean, default=False)
    diagnostico = db.Column(db.Enum('ECNE', 'Lesión post-traumática', 'Mielomeningocele', 'Esclerosis Múltiple', 'Escoliosis Leve', 'Secuelas de ACV', 'Discapacidad Intelectual', 'Trastorno del Espectro Autista', 'Trastorno del Aprendizaje', 'Trastorno por Déficit de Atención/Hiperactividad',     'Trastorno de la Comunicación', 'Trastorno de Ansiedad', 'Síndrome de Down', 'Retraso Madurativo', 'Psicosis', 'Trastorno de Conducta', 'Trastornos del ánimo y afectivos', 'Trastorno Alimentario', 'OTRO'))
    otro = db.Column(db.String(100), default=None)
    tipo_de_discapacidad = db.Column(db.Enum('Mental', 'Motora', 'Sensorial', 'Viceral'))
    asignacion_familiar = db.Column(db.Boolean)
    assignments = db.relationship('Assignment', secondary='rider_assignment', backref='riders')
    pension = db.Column(db.Enum('Provincial', 'Nacional'), default=None)
    obra_social = db.Column(db.String(100))
    numero_afiliado = db.Column(db.String(30))
    curatela = db.Column(db.Boolean)
    observaciones = db.Column(db.Text)
    institucion_escolar = db.Column(db.String(100))
    direccion_institucion = db.Column(db.String(255))
    grado = db.Column(db.String(100))
    telefono_institucion = db.Column(db.String(50))
    observaciones_institucion = db.Column(db.Text)
    tutores = db.relationship('Tutor', secondary='rider_tutor', backref='riders')
    propuesta_trabajo = db.Column(db.Enum('Hipoterapia', 'Monta Terapéutica', 'Deporte Ecuestre Adaptado', 'Actividades Recreativas', 'Equitación', name='assigned_activities'))
    condicion = db.Column(db.Enum('Regular', 'De Baja'))
    sede = db.Column(db.Enum('CASJ', 'HLP', 'OTRO'))
    #TERMIANR DIAS
    dias = db.relationship('Day', secondary='rider_day', backref='riders')
    documentacion = db.Column(JSON)

    def __repr__(self):
        return f'<Jinete/Amazona {self.nombre} {self.apellido}>'
