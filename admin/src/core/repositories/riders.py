from flask import current_app
from src.core.database import db
from src.core.models.rider import Rider, rider_tutor
from src.core.repositories import assignment as assignment_repository
from src.core.repositories import day as day_repository
from src.core.repositories import tutor as tutor_repository

def create_rider(**kwargs):
    rider = Rider(**kwargs)
    try:
        with db.session.begin_nested():
            db.session.add(rider)
            _update_professional_assignments(rider, kwargs)
            _update_family_assignments(rider, kwargs)
            _update_days(rider, kwargs)
            _update_tutors(rider, kwargs)
            _update_basic_fields(rider, kwargs)

        db.session.commit()
        return rider
    except Exception as e:
        db.session.rollback()
        return None

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
    rider = Rider.query.filter(Rider.name == name).first()
    return rider

def find_rider_by_apellido(surname):
    rider = Rider.query.filter(Rider.surname == surname).first()
    return rider

def find_rider_by_dni(dni):
    rider = Rider.query.filter(Rider.dni == dni).first()
    return rider

def find_rider_by_professionals(professionals):
    rider = Rider.query.filter(Rider.professionals == professionals).first()
    return rider

def update_rider(id, **kwargs):
    rider = Rider.query.filter(Rider.id == id).first()
    if not rider:
        return False

    try:
        with db.session.begin_nested():
            _update_professional_assignments(rider, kwargs)
            _update_family_assignments(rider, kwargs)
            _update_days(rider, kwargs)
            _update_tutors(rider, kwargs)
            _update_basic_fields(rider, kwargs)

        db.session.commit()
        return True
    except Exception as e:
        db.session.rollback()
        return False

def _update_professional_assignments(rider, data):
    """Update professional assignments for the rider."""
    professional_fields = {
        'therapist_teacher_id': None,
        'horse_conductor_id': None,
        'horse_id': None,
        'track_assistant_id': None
    }

    for field, _ in professional_fields.items():
        value = data.get(field)
        if value and value != 'None':
            setattr(rider, field, value)

def _update_family_assignments(rider, data):
    """Update family assignments for the rider."""
    if data.get('family_assignment'):
        assignments = data.get('assignments', [])
        assignment_ids = assignment_repository.get_assignment_ids_by_names(assignments)
        rider.assignments = assignment_repository.get_assignments(assignment_ids)

def _update_days(rider, data):
    """Update rider's days."""
    if days := data.get('days'):
        rider.days = day_repository.get_days(days)

def _update_tutors(rider, data):
    """Update rider's tutors."""
    tutors_data = data.get('tutors', [])
    if not tutors_data:
        return

    tutors = []
    for tutor_data in tutors_data:
        tutor = _process_tutor_data(tutor_data)
        if tutor:
            tutors.append((tutor, tutor_data.get('relationship')))

    _update_rider_tutors(rider, tutors)

def _process_tutor_data(tutor_data):
    """Process individual tutor data and return tutor object."""
    required_fields = {'name', 'surname', 'dni'}
    if not all(tutor_data.get(field) for field in required_fields):
        return None

    tutor = tutor_repository.get_tutor(tutor_data['dni'])
    if not tutor:
        tutor = tutor_repository.create_tutor(**tutor_data)
    else:
        for field in ['name', 'surname', 'address', 'cellphone',
                     'email', 'educational_level', 'occupation']:
            if value := tutor_data.get(field):
                setattr(tutor, field, value)

    return tutor

def _update_rider_tutors(rider, tutors):
    """Update the rider-tutor relationships."""
    try:
        db.session.execute(rider_tutor.delete().where(rider_tutor.c.rider_id == rider.id))

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

def _update_basic_fields(rider, data):
    """Update basic fields of the rider."""
    for key, value in data.items():
        if hasattr(rider, key):
            setattr(rider, key, value)

def delete_rider(id):
    rider = Rider.query.filter(Rider.id == id).first()
    if not rider:
        return False
    db.session.delete(rider)
    db.session.commit()
    return True

def get_rider(id):
    rider = Rider.query.filter(Rider.id == id).first()
    return rider

def has_assignment(rider, assignment_name):
    return any(assignment.name == assignment_name for assignment in rider.assignments)
