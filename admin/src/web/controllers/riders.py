import re
from flask import Blueprint, redirect, render_template, request, url_for, flash
from src.core.repositories import riders as rider_repository
from src.core.repositories import employee as employee_repository
from src.core.repositories import horse as horse_repository
from src.core.repositories import day as day_repository
from src.core.repositories import tutor as tutor_repository
from src.web.helpers.auth import has_permission
from src.core.validation.models.rider import RiderValidator
from src.web.helpers.flash import flash_validation_errors
from src.core.repositories import assignment as assignments_repository


bp = Blueprint("riders", __name__, url_prefix="/riders")

# list riders


@bp.get("/")
@has_permission("rider_index")  # permiso para listar jinetes y amazonas
def index():
    search = request.args.get("search", "")
    sort_by = request.args.get("sort_by", "name")
    direction = request.args.get("direction", "asc")
    page = int(request.args.get("page", 1))

    riders = rider_repository.list_riders(search, sort_by, direction, page)

    if not riders.items:
        flash("No se encontraron jinetes/amazonas.", "info")
    return render_template("riders/index.html", pagination=riders)


# Register
@bp.get("/create")
@has_permission("rider_create")
def register():

    diagnoses = rider_repository.get_diagnoses()
    work_proposals = rider_repository.get_work_proposals()
    disability_types = rider_repository.get_disability_types()
    pension_types = rider_repository.get_pensions()
    headquarters = rider_repository.get_headquarters()
    conditions = rider_repository.get_conditions()

    all_days = day_repository.list_days()
    jb = ['Profesor de Equitación', 'Terapeuta']

    profesor_therapist = employee_repository.get_employees_by_job_positions(jb)

    conductor = employee_repository.get_employees_by_job_positions('Conductor')
    auxiliar_pista = employee_repository.get_employees_by_job_positions(
        'Auxiliar de pista')
    all_horses = horse_repository.list_horses()

    diagnoses = rider_repository.get_diagnoses()
    assignments = assignments_repository.list_assignments()

    return render_template("riders/form.html", is_update=False, title='Crear Jinete/Amazona', all_days=all_days, all_horses=all_horses, tutor_cant=0, tutors=[], profesor_therapist=profesor_therapist, conductor=conductor, auxiliar_pista=auxiliar_pista, diagnoses=diagnoses, work_proposals=work_proposals, disability_types=disability_types, pension_types=pension_types, headquarters=headquarters, conditions=conditions, assignments=assignments)

# Create rider


@bp.post("/create")
@has_permission("rider_create")
def create():
    params = request.form.to_dict()
    params['days'] = request.form.getlist('days')
    assignments = request.form.getlist('assignments')
    params['tutors'] = [
        {
            'relationship': request.form.get(f'tutors[{i}][relationship]'),
            'name': request.form.get(f'tutors[{i}][name]'),
            'surname': request.form.get(f'tutors[{i}][surname]'),
            'dni': request.form.get(f'tutors[{i}][dni]'),
            'address': request.form.get(f'tutors[{i}][address]'),
            'cellphone': request.form.get(f'tutors[{i}][cellphone]'),
            'email': request.form.get(f'tutors[{i}][email]'),
            'educational_level': request.form.get(f'tutors[{i}][educational_level]'),
            'occupation': request.form.get(f'tutors[{i}][occupation]')
        }
        for i in range(2)  # Solo 2 tutores
    ]
    print("tutores asd", params['tutors'])

    if assignments == 'None':
        assignments = None


    for field in ['therapist_teacher_id', 'horse_conductor_id', 'horse_id', 'track_assistant_id']:
        if params.get(field) == 'None':
            params[field] = None

    validator = RiderValidator()
    errors = validator.validate_create(params)

    if errors:
        flash_validation_errors(errors)
        return redirect(url_for("riders.register"))

    scholarship = 'scholarship' in request.form
    guardianship = 'guardianship' in request.form
    family_assignment = 'family_assignment' in request.form
    disability_certificate = 'disability_certificate' in request.form
    other = None

    
   

    if 'diagnosis' in params:
        diagnosis = params['diagnosis']
        if diagnosis == 'OTRO':
            other = params['other']
    else:
        diagnosis = 'None'

    if 'disability_type' in params:
        disability_type = params['disability_type']
    else:
        disability_type = 'None'

    if 'pension' in params:
        pension = params['pension']
    else:
        pension = 'No'

    rider = rider_repository.create_rider(
        name=params['name'],
        surname=params['surname'],
        dni=params['dni'],
        age=params['age'],
        birthdate=params['birthdate'],
        birth_place=params['birth_place'],
        address=params['address'],
        phone=params['phone'],
        emergency_contact=params['emergency_contact'],
        emergency_contact_phone_number=params['emergency_contact_phone_number'],
        scholarship=scholarship,
        scholarship_percentage=params['scholarship_percentage'],
        professionals=params['professionals'],
        disability_certificate=disability_certificate,
        diagnosis=diagnosis,
        other=other,
        disability_type=disability_type,
        family_assignment=family_assignment,
        pension=pension,
        health_insurance=params['health_insurance'],
        affiliate_number=params['affiliate_number'],
        guardianship=guardianship,
        observations=params['observations'],
        school_institution=params['school_institution'],
        institution_address=params['institution_address'],
        grade=params['grade'],
        institution_phone=params['institution_phone'],
        institution_observations=params['institution_observations'],
        work_proposal=params['work_proposal'],
        condition=params['condition'],
        headquarters=params['headquarters'],
        therapist_teacher_id=params['therapist_teacher_id'],
        horse_conductor_id=params['horse_conductor_id'],
        horse_id=params['horse_id'],
        track_assistant_id=params['track_assistant_id'],
        days=params['days'],
        tutors=params['tutors'],
        assignments=assignments # Agregar assignments
    )


    flash("Jinete/Amazona creado con éxito.", "info")
    return redirect(url_for("riders.index"))

# Show rider


@bp.get("/<int:id>/show")
@has_permission("rider_show")
def show(id):
    rider = rider_repository.get_rider(id)
    if not rider:
        flash("Jinete/Amazona no encontrado.", "error")
        return redirect(url_for("riders.index"))
    tutors_with_relationship = tutor_repository.get_tutors_with_relationships(
        id)
    return render_template("riders/show.html", rider=rider, tutors_with_relationship=tutors_with_relationship)

# Editar jinete/amazona


@bp.get("/<int:id>/update")
@has_permission("rider_update")
def edit(id):
    diagnoses = rider_repository.get_diagnoses()
    work_proposals = rider_repository.get_work_proposals()
    disability_types = rider_repository.get_disability_types()
    pension_types = rider_repository.get_pensions()
    headquarters = rider_repository.get_headquarters()
    conditions = rider_repository.get_conditions()

    all_days = day_repository.list_days()
    jb = ['Profesor de Equitación', 'Terapeuta']

    profesor_therapist = employee_repository.get_employees_by_job_positions(jb)

    conductor = employee_repository.get_employees_by_job_positions('Conductor')
    auxiliar_pista = employee_repository.get_employees_by_job_positions(
        'Auxiliar de pista')
    all_horses = horse_repository.list_horses()

    rider = rider_repository.get_rider(id)
    if not rider:
        flash("Jinete/Amazona no encontrado.", "error")
        return redirect(url_for("riders.index"))
    tutor_cant = len(list(rider.tutors))
    tutors = tutor_repository.get_tutors_with_relationships(id)   
    assignments = assignments_repository.list_assignments()
  
    return render_template("riders/form.html", is_update=True, title='Actualizar Jinete/Amazona', rider=rider, all_days=all_days, all_horses=all_horses, tutor_cant=tutor_cant, tutors=tutors, profesor_therapist=profesor_therapist, conductor=conductor, auxiliar_pista=auxiliar_pista, diagnoses=diagnoses, work_proposals=work_proposals, disability_types=disability_types, pension_types=pension_types, headquarters=headquarters, conditions=conditions, assignments=assignments)


@bp.post("/<int:id>/update")
@has_permission("rider_update")
def update(id):
    params = request.form.to_dict()
    params['days'] = request.form.getlist('days')
    params['assignments'] = request.form.getlist('assignments')
    params['tutors'] = [
        {
            'relationship': request.form.get(f'tutors[{i}][relationship]'),
            'name': request.form.get(f'tutors[{i}][name]'),
            'surname': request.form.get(f'tutors[{i}][surname]'),
            'dni': request.form.get(f'tutors[{i}][dni]'),
            'address': request.form.get(f'tutors[{i}][address]'),
            'cellphone': request.form.get(f'tutors[{i}][cellphone]'),
            'email': request.form.get(f'tutors[{i}][email]'),
            'educational_level': request.form.get(f'tutors[{i}][educational_level]'),
            'occupation': request.form.get(f'tutors[{i}][occupation]')
        }
        for i in range(2)  # Solo 2 tutores
    ]

    for field in ['therapist_teacher_id', 'horse_conductor_id', 'horse_id', 'track_assistant_id']:
        if params.get(field) == 'None':
            params[field] = None

    validator = RiderValidator(id)
    errors = validator.validate_update(params)

    if errors:
        flash_validation_errors(errors)
        return redirect(url_for("riders.edit", id=id))

    scholarship = 'scholarship' in request.form
    guardianship = 'guardianship' in request.form
    family_assignment = 'family_assignment' in request.form
    disability_certificate = 'disability_certificate' in request.form
    other = None

    if 'diagnosis' in params:
        diagnosis = params['diagnosis']
        if diagnosis == 'OTRO':
            other = params['other']
    else:
        diagnosis = 'None'

    if 'disability_type' in params:
        disability_type = params['disability_type']
    else:
        disability_type = 'None'

    if 'pension' in params:
        pension = params['pension']
    else:
        pension = 'No'

    rider = rider_repository.get_rider(id)
    if not rider:
        flash("Jinete/Amazona no encontrado", "error")
        return redirect(url_for("riders.index"))

    if rider_repository.update_rider(
        id=id,
        name=params['name'],
        surname=params['surname'],
        dni=params['dni'],
        age=params['age'],
        birthdate=params['birthdate'],
        birth_place=params['birth_place'],
        address=params['address'],
        phone=params['phone'],
        emergency_contact=params['emergency_contact'],
        emergency_contact_phone_number=params['emergency_contact_phone_number'],
        scholarship=scholarship,
        scholarship_percentage=params['scholarship_percentage'],
        professionals=params['professionals'],
        disability_certificate=disability_certificate,
        diagnosis=diagnosis,
        other=other,
        disability_type=disability_type,
        family_assignment=family_assignment,
        pension=pension,
        health_insurance=params['health_insurance'],
        affiliate_number=params['affiliate_number'],
        guardianship=guardianship,
        observations=params['observations'],
        school_institution=params['school_institution'],
        institution_address=params['institution_address'],
        grade=params['grade'],
        institution_phone=params['institution_phone'],
        institution_observations=params['institution_observations'],
        work_proposal=params['work_proposal'],
        condition=params['condition'],
        headquarters=params['headquarters'],
        therapist_teacher_id=params['therapist_teacher_id'],
        horse_conductor_id=params['horse_conductor_id'],
        horse_id=params['horse_id'],
        track_assistant_id=params['track_assistant_id'],
        days=params['days'],
        tutors=params['tutors'],
        assignments=params['assignments']
    ):
        flash("Jinete/Amazona actualizado con éxito.", "success")
        return redirect(url_for("riders.index"))
    else:
        flash("Error al actualizar.", "error")
        return redirect(url_for("riders.index"))

# destroy rider


@bp.get("/<int:id>/delete")
@has_permission("rider_destroy")
def delete(id):
    if rider_repository.delete_rider(id):
        flash("Jinete/Amazona eliminado con éxito.", "info")
        return redirect(url_for("riders.index"))
    else:
        flash("Jinete/Amazona no encontrado.", "error")
        return redirect(url_for("riders.index"))
