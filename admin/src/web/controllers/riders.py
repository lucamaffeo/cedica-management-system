import re
from flask import Blueprint, redirect, render_template, request, session, url_for, flash
from src.core.repositories import riders as rider_repository
from src.core.models.assignment import Assignment
from src.core.models.tutor import Tutor
from src.core.models.day import Day
from src.core.models.employee import Employee
from src.core.models.horse import Horse
from src.core.models.rider import rider_tutor
from src.core.repositories.assignment import get_assignment_ids_by_names
from src.web.helpers.auth import has_permission
from werkzeug.utils import secure_filename
from os import fstat
from flask import current_app
from src.core.database import db


bp = Blueprint("riders", __name__, url_prefix="/riders")

#list riders
@bp.get("/")
@has_permission("rider_index") #permiso para listar jinetes y amazonas
def index():
    search = request.args.get("search", "")
    sort_by = request.args.get("sort_by", "name")
    direction = request.args.get("direction", "asc")
    page = int(request.args.get("page", 1))
    items_per_page = 5

    riders = rider_repository.list_riders(search, sort_by, direction, page, items_per_page)

    if not riders.items:
        flash("No se encontraron jinetes/amazonas.", "info")
    return render_template("riders/index.html", pagination=riders)


# Register
@bp.get("/create")
@has_permission("rider_create")
def register():
    all_days = Day.query.all()
    all_employees = Employee.query.all()
    all_horses = Horse.query.all()
    return render_template("riders/form.html", is_update=False, title='Crear Jinete/Amazona', all_days=all_days, all_employees=all_employees, all_horses=all_horses, tutor_cant=0, tutors=[])

# Create rider
@bp.post("/create")
@has_permission("rider_create")
def create():

    scholarship = 'scholarship' in request.form
    guardianship = 'guardianship' in request.form
    family_assignment = 'family_assignment' in request.form
    disability_certificate = 'disability_certificate' in request.form
    params = request.form
    required_fields = ['name', 'surname', 'dni', 'age', 'birthdate', 'birth_place', 'address',
                       'phone', 'emergency_contact', 'emergency_contact_phone_number',
                        'professionals', 'health_insurance', 'affiliate_number', 'observations', 
                        'school_institution', 'institution_address', 'grade', 'institution_phone',
                        'institution_observations', 'work_proposal', 'condition', 'headquarters'
                       ]
    for field in required_fields:
        if field not in params:
            flash(f"El campo {field} es requerido.", "error")
            return redirect(url_for("riders.register"))

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

    tutors_ids = request.form.getlist('tutors_')
    days = request.form.getlist('days')
    print()
    print()
    print()
    print(days)
    print()
    print()
    print()

    # Validar el DNI (solo números y puntos)
    #if not re.match(r'^[\d.]+$', params['dni']):
    #   flash("El DNI solo puede contener números y puntos.", "error")
    #   return redirect(url_for("riders.register"))

    # Validar si el DNI ya está registrado
    dni = params['dni']
    existing_rider_dni = rider_repository.find_rider_by_dni(dni)
    if existing_rider_dni:
        flash("El DNI ya está registrado por otro jinete o amazona.", "error")
        return redirect(url_for("riders.index"))

    rider = rider_repository.create_rider(
        name = params['name'],
        surname = params['surname'],
        dni = params['dni'],
        age = params['age'],
        birthdate = params['birthdate'],
        birth_place = params['birth_place'],
        address = params['address'],
        phone = params['phone'],
        emergency_contact = params['emergency_contact'],
        emergency_contact_phone_number = params['emergency_contact_phone_number'],
        scholarship = scholarship,
        scholarship_percentage = params['scholarship_percentage'],
        professionals = params['professionals'],
        disability_certificate = disability_certificate,
        diagnosis = diagnosis,
        other = other,
        disability_type = disability_type,
        family_assignment = family_assignment,
        pension = pension,
        health_insurance = params['health_insurance'],
        affiliate_number = params['affiliate_number'],
        guardianship = guardianship,
        observations = params['observations'],
        school_institution = params['school_institution'],
        institution_address = params['institution_address'],
        grade = params['grade'],
        institution_phone = params['institution_phone'],
        institution_observations = params['institution_observations'],
        work_proposal = params['work_proposal'],
        condition = params['condition'],
        headquarters = params['headquarters'],
    )  

    if params['therapist_teacher_id'] != None and params['therapist_teacher_id'] != 'None':
        rider.therapist_teacher_id = params['therapist_teacher_id']
    
    if params['horse_conductor_id'] != None and params['horse_conductor_id'] != 'None':
        rider.horse_conductor_id = params['horse_conductor_id']

    if params['horse_id'] != None and params['horse_id'] != 'None':
        rider.horse_id = params['horse_id']

    if params['track_assistant_id'] != None and params['track_assistant_id'] != 'None':
        rider.track_assistant_id = params['track_assistant_id']


    if family_assignment == True:
        assignments = request.form.getlist('assignments')
        assignment_ids = get_assignment_ids_by_names(assignments)
        rider.assignments = Assignment.query.filter(Assignment.id.in_(assignment_ids)).all()

    if tutors_ids:
        for tutor_id in tutors_ids:
            tutor = Tutor.query.get(tutor_id)
            if tutor: 
                rider.tutors.append(tutor)  
            else:
                flash(f"Tutor con ID {tutor_id} no encontrado.", "error")
    if days != None:
        for day_id in days:
            day = Day.query.get(day_id)
            if day: 
                rider.days.append(day)  
            else:
                flash(f"Día con ID {day_id} no encontrado.", "error")

    # Guardar cambios en la base de datos -- NO SE SI ES NECESARIO !!! VER
    db.session.commit()
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
    tutors_with_relationship = db.session.query(
        Tutor, rider_tutor.c.relationship
    ).join(
        rider_tutor, Tutor.id == rider_tutor.c.tutor_id
    ).filter(
        rider_tutor.c.rider_id == id
    ).all()
    return render_template("riders/show.html", rider=rider, tutors_with_relationship=tutors_with_relationship)

# Editar jinete/amazona
@bp.get("/<int:id>/update")
@has_permission("rider_update")
def edit(id):
    all_days = Day.query.all()
    all_employees = Employee.query.all()
    all_horses = Horse.query.all()

    rider = rider_repository.get_rider(id)
    if not rider:
        flash("Jinete/Amazona no encontrado.", "error")
        return redirect(url_for("riders.index"))
    tutor_cant = len(rider.tutors)
    tutors = db.session.query(
        Tutor, rider_tutor.c.relationship
    ).join(
        rider_tutor, Tutor.id == rider_tutor.c.tutor_id
    ).filter(
        rider_tutor.c.rider_id == id
    ).all()
    print('AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA', tutors)
    return render_template("riders/form.html", is_update=True, title='Actualizar Jinete/Amazona', rider=rider, all_days=all_days, all_employees=all_employees, all_horses=all_horses, tutor_cant=tutor_cant, tutors=tutors)

@bp.post("/<int:id>/update")
@has_permission("rider_update")
def update(id):
    rider = rider_repository.get_rider(id)
    if not rider:
        flash("Jinete/Amazona no encontrado.", "error")
        return redirect(url_for("riders.index"))

    params = request.form 
    scholarship = 'scholarship' in request.form

    other = None    
    if 'diagnosis' in params:
        diagnosis = params['diagnosis']
        if diagnosis == 'OTRO':
            other = params['other']
    else:
        diagnosis = None

    if 'disability_type' in params:
        disability_type = params['disability_type']
    else:
        disability_type = None
        
    if params['family_assignment'] == 'True':
        assignments_ids = request.form.getlist('assignment_id')

    tutors_ids = request.form.getlist('tutor_id')
    days_ids = request.form.getlist('day_id')

    if 'therapist_teacher_id' in params:
        therapist_teacher_id = params['therapist_teacher_id']
    else:
        therapist_teacher_id = None
    
    if 'horse_conductor_id' in params:
        horse_conductor_id = params['horse_conductor_id']
    else:
        horse_conductor_id = None

    if 'horse_id' in params:
        horse_id = params['horse_id']
    else:
        horse_id = None

    if 'track_assistant_id' in params:
        track_assistant_id = params['track_assistant_id']
    else:
        track_assistant_id = None

    # Validar el DNI (solo números y puntos)
    #if not re.match(r'^[\d.]+$', params['dni']):
    #   flash("El DNI solo puede contener números y puntos.", "error")
    #   return redirect(url_for("riders.register"))

     # Validar si el DNI ya está registrado por otro jinete/amazona
    dni = params['dni']
    if dni and dni != rider.dni:
        existing_rider_dni = rider_repository.find_rider_by_dni(dni)
        if existing_rider_dni:
            flash("El DNI ya está registrado por otro jinete o amazona.", "error")
            return redirect(url_for("riders.edit", id=id))


    # Actualizar el jinete
    rider = rider_repository.update_rider(
        name = params['name'],
        surname = params['surname'],
        dni = params['dni'],
        age = params['age'],
        birthdate = params['birthdate'],
        birth_place = params['birth_place'],
        address = params['address'],
        phone = params['phone'],
        emergency_contact = params['emergency_contact'],
        emergency_contact_phone_number = params['emergency_contact_phone_number'],
        scholarship = scholarship,
        scholarship_percentage = params['scholarship_percentage'],
        professionals = params['professionals'],
        disability_certificate = params['disability_certificate'],
        diagnosis = diagnosis,
        other = other,
        disability_type = disability_type,
        family_assignment = params['family_assignment'],
        pension = params['pension'],
        health_insurance = params['health_insurance'],
        affiliate_number = params['affiliate_number'],
        guardianship = params['guardianship'],
        observations = params['observations'],
        school_institution = params['school_institution'],
        institution_address = params['institution_address'],
        grade = params['grade'],
        institution_phone = params['institution_phone'],
        institution_observations = params['institution_observations'],
        work_proposal = params['work_proposal'],
        condition = params['condition'],
        headquarters = params['headquarters'],
        therapist_teacher_id = therapist_teacher_id,
        horse_conductor_id = horse_conductor_id,
        horse_id = horse_id,
        track_assistant_id = track_assistant_id
    )
    # Manejar la carga de archivos

    if assignments_ids:
        for assignment_id in assignments_ids:
            assignment = Assignment.query.get(assignment_id)  # Busca la asignación por ID
            if assignment:  # Asegúrate de que la asignación existe
                rider.assignments.append(assignment)  # Agrega la asignación a la relación
            else:
                flash(f"Asignación con ID {assignment_id} no encontrada.", "error")
    if tutors_ids:
        for tutor_id in tutors_ids:
            tutor = Tutor.query.get(tutor_id)
            if tutor: 
                rider.tutors.append(tutor)  
            else:
                flash(f"Tutor con ID {tutor_id} no encontrado.", "error")
    if days_ids:
        for day_id in days_ids:
            day = Day.query.get(day_id)
            if day: 
                rider.days.append(day)  
            else:
                flash(f"Día con ID {day_id} no encontrado.", "error")

    # Guardar cambios en la base de datos -- NO SE SI ES NECESARIO !!! VER
    db.session.commit()
    flash("Jinete/Amazona actualizado con éxito.", "success")
    return redirect(url_for("riders.index"))

# destroy rider
@bp.get("/<int:id>/delete")
@has_permission("rider_destroy")
def delete(id):
    rider = rider_repository.get_rider(id)
    if not rider:
        flash("Jinete/Amazona no encontrado.", "error")
        return redirect(url_for("riders.index"))

    rider_repository.delete_rider(id)
    flash("Jinete/Amazona eliminado con éxito.", "info")
    return redirect(url_for("riders.index"))