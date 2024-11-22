from flask import current_app
from src.core.database import db
from src.core.models.rider import Rider, rider_tutor
from src.core.repositories import assignment as assignment_repository
from src.core.repositories import day as day_repository
from src.core.repositories import tutor as tutor_repository
from src.core.repositories import document as document_repository


def create_rider(**kwargs):
    """Crea un jinete y maneja las relaciones con asignaciones, días y tutores."""
    days = kwargs.pop('days', [])
    tutors = kwargs.pop('tutors', [])
    assignments = kwargs.pop('assignments', [])

    rider = Rider(**kwargs)
    db.session.add(rider)

    _update_days(rider, {'days': days})
    _update_tutors(rider, {'tutors': tutors})
    _update_family_assignments(rider, {'assignments': assignments})

    db.session.commit()
    return rider


def get_diagnoses():
    return Rider.diagnosis.property.columns[0].type.enums


def get_work_proposals():
    return Rider.work_proposal.property.columns[0].type.enums


def get_disability_types():
    return Rider.disability_type.property.columns[0].type.enums


def get_pensions():
    return Rider.pension.property.columns[0].type.enums


def get_headquarters():
    return Rider.headquarters.property.columns[0].type.enums


def get_conditions():
    return Rider.condition.property.columns[0].type.enums


def list_riders(search='', sort_by='name', direction='asc', page=1):
    query = Rider.query

    if search:
        query = query.filter(
            (Rider.name.ilike(f'%{search}%')) |
            (Rider.surname.ilike(f'%{search}%')) |
            (Rider.dni.ilike(f'%{search}%')) |
            (Rider.professionals.ilike(f'%{search}%'))
        )

    items_per_page = current_app.config.get('ITEMS_PER_PAGE')

    # Aplicar ordenación
    if sort_by in ['name', 'surname']:
        if direction == 'asc':
            query = query.order_by(getattr(Rider, sort_by).asc())
        else:
            query = query.order_by(getattr(Rider, sort_by).desc())

    pagination_riders = query.paginate(page=page, per_page=items_per_page, error_out=False)

    return pagination_riders


def find_rider_by_name(name):
    return Rider.query.filter(Rider.name == name).first()


def find_rider_by_apellido(surname):
    return Rider.query.filter(Rider.surname == surname).first()


def find_rider_by_dni(dni):
    return Rider.query.filter(Rider.dni == dni).first()


def find_rider_by_professionals(professionals):
    return Rider.query.filter(Rider.professionals == professionals).first()


def update_rider(id, **kwargs):
    rider = Rider.query.filter(Rider.id == id).first()
    if not rider:
        return False

    days = kwargs.pop('days', [])
    tutors = kwargs.pop('tutors', [])
    assignments = kwargs.pop('assignments', [])

    for key, value in kwargs.items():
        setattr(rider, key, value)

    _update_days(rider, {'days': days})
    _update_tutors(rider, {'tutors': tutors})
    _update_family_assignments(rider, {'assignments': assignments})

    db.session.commit()
    return True




def _update_family_assignments(rider, data):
    """Actualizar las asignaciones familiares del jinete."""
    assignments = data.get('assignments', [])
    assignment_ids = assignment_repository.get_assignment_ids_by_names(assignments)
    rider.assignments = assignment_repository.get_assignments(assignment_ids)


def _update_days(rider, data):
    """Actualizar los días del jinete."""
    if days := data.get('days'):
        rider.days = day_repository.get_days(days)


def _update_tutors(rider, data):
    """Actualizar los tutores del jinete."""
    tutors_data = data.get('tutors', [])
    if not tutors_data:
        return

    # Crear una lista para almacenar los tutores y sus relaciones
    tutors = []
    for tutor_data in tutors_data:
        # Procesamos cada tutor y sus datos
        relationship = tutor_data.pop('relationship', None)
        tutor = _process_tutor_data(tutor_data)
        if tutor:
            print(relationship,"aaaaaa")
            if relationship:  # Asegurarnos de que la relación no sea vacía
                tutors.append((tutor, relationship))

    # Ahora actualizamos la tabla intermedia para los tutores
    _update_rider_tutors(rider, tutors)


def _process_tutor_data(tutor_data):
    """Procesar los datos de un tutor y devolver el objeto tutor."""
    required_fields = {'name', 'surname', 'dni'}
    if not all(tutor_data.get(field) for field in required_fields):
        return None  # Si no se completan todos los campos requeridos, no procesamos el tutor

    # Buscar el tutor en la base de datos por su dni
    tutor = tutor_repository.get_tutor(tutor_data['dni'])
    if not tutor:
        # Si el tutor no existe, lo creamos
        tutor = tutor_repository.create_tutor(**tutor_data)
    else:
        # Si el tutor ya existe, actualizamos sus datos
        for field in ['name', 'surname', 'address', 'cellphone', 'email', 'educational_level', 'occupation']:
            if value := tutor_data.get(field):
                setattr(tutor, field, value)
    
    # Retornar el objeto tutor
    return tutor


def _update_rider_tutors(rider, tutors):
    """Actualizar la relación entre el jinete y los tutores."""
    try:
        # Limpiar las relaciones previas entre el jinete y los tutores
        db.session.execute(rider_tutor.delete().where(rider_tutor.c.rider_id == rider.id))

        # Insertar las nuevas relaciones de tutores
        for tutor, relationship in tutors:
            if tutor and tutor.id:
                db.session.execute(
                    rider_tutor.insert().values(
                        rider_id=rider.id,
                        tutor_id=tutor.id,
                        relationship=relationship
                    )
                )
    except Exception as e:
        db.session.rollback()
        raise e




def delete_rider(id):
    rider = Rider.query.filter(Rider.id == id).first()
    if not rider:
        return False

    if rider.documents:
        for document in rider.documents:
            document_repository.delete_document(document.id)

    db.session.delete(rider)
    db.session.commit()
    return True


def get_rider(id):
    return Rider.query.filter(Rider.id == id).first()


def has_assignment(rider, assignment_name):
    return any(assignment.name == assignment_name for assignment in rider.assignments)
