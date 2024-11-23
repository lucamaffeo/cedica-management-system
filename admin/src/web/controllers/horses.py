from flask import Blueprint, redirect, render_template, request, url_for, flash
from src.core.repositories import horse as horse_repository
from src.core.repositories import document as document_repository
from src.core.repositories import employee as employee_repository
from src.web.helpers.auth import has_permission
from src.core.repositories.employee import get_employees_by_job_positions
from src.core.database import db
from src.core.validation.models.horse import HorseValidator


bp = Blueprint("horses", __name__, url_prefix="/horses")

# list horses


@bp.get("/")
@has_permission("horse_index")  # permiso para listar caballos
def index():
    """
    Renderiza la página de índice de caballos con paginación y filtros.
    """
    search = request.args.get("search", "")
    assigned_activities_ja = request.args.get("assigned_activities_ja", None)
    sort_by = request.args.get("sort_by", "name")
    direction = request.args.get("direction", "asc")
    page = int(request.args.get("page", 1))

    horses = horse_repository.list_horses(
        search, assigned_activities_ja, sort_by, direction, page)

    activities = horse_repository.get_activities()

    if not horses.items:
        flash("No se encontraron caballos.", "info")
    return render_template("horses/index.html", pagination=horses, activities=activities)

# register horse


@bp.get("/create")
@has_permission("horse_create")
def register():
    """
    Renderiza el formulario para crear un nuevo caballo.
    """
    job_positions = ["Conductor", "Entrenador de Caballos"]
    trainers = get_employees_by_job_positions(job_positions)
    activities = horse_repository.get_activities()
    genders = horse_repository.get_genders()
    purchase_donation = horse_repository.get_purchase_donation()

    return render_template("horses/form.html", is_update=False, title='Crear Caballo', trainers=trainers, activities=activities, genders=genders, purchase_donation=purchase_donation)

# Create horse


@bp.post("/create")
@has_permission("horse_create")
def create():
    """
    Crea un nuevo caballo basado en los datos del formulario.
    """
    params = request.form
    validator = HorseValidator()
    errors = validator.validate_create(params)
    if errors:
        for error in errors:
            flash(f"{error.field}: {error.message}", "error")
        return redirect(url_for("horses.register"))

    trainer_ids = request.form.getlist('trainer_id')

    horse = horse_repository.create_horse(
        name=params['name'],
        birth_date=params['birth_date'] or None,
        gender=params['gender'],
        breed=params['breed'],
        coat=params['coat'],
        purchase_donation=params['purchase_donation'],
        entry_date=params['entry_date'],
        assigned_location=params['assigned_location'],
        assigned_activities_ja=params['assigned_activities_ja'],
        trainer_ids=trainer_ids
    )
    flash("Caballo creado con éxito.", "success")
    return redirect(url_for("horses.index"))

# show horse


@bp.get("/<int:id>/show")
@has_permission("horse_show")
def show(id):
    """
    Muestra los detalles de un caballo específico.
    
    :param id: ID del caballo a mostrar.
    """
    horse = horse_repository.get_horse(id)
    if not horse:
        flash("Caballo no encontrado.", "error")
        return redirect(url_for("horses.index"))
    return render_template("horses/show.html", horse=horse)

# Edit horse


@bp.get("/<int:id>/update")
@has_permission("horse_update")
def edit(id):
    """
    Renderiza el formulario para editar un caballo existente.
    
    :param id: ID del caballo a editar.
    """
    horse = horse_repository.get_horse(id)
    job_positions = ["Conductor", "Entrenador de Caballos"]
    trainers = get_employees_by_job_positions(job_positions)
    activities = horse_repository.get_activities()
    genders = horse_repository.get_genders()
    purchase_donation = horse_repository.get_purchase_donation()

    if not horse:
        flash("Caballo no encontrado.", "error")
        return redirect(url_for("horses.index"))

    associated_trainer_ids = [trainer.id for trainer in horse.association]

    return render_template("horses/form.html", is_update=True, title='Editar Caballo', horse=horse, trainers=trainers, associated_trainer_ids=associated_trainer_ids, activities=activities, genders=genders, purchase_donation=purchase_donation)

# update horse


@bp.post("/<int:id>/update")
@has_permission("horse_update")
def update(id):
    """
    Actualiza un caballo existente basado en los datos del formulario.
    
    :param id: ID del caballo a actualizar.
    """
    params = request.form
    validator = HorseValidator()
    errors = validator.validate_update(params, id)
    if errors:
        for error in errors:
            flash(f"{error.field}: {error.message}", "error")
        return redirect(url_for("horses.edit", id=id))

    # Obtener los nuevos IDs de entrenadores seleccionados desde el formulario
    trainer_ids = request.form.getlist('trainer_id')

    if horse_repository.update_horse(
        horse_id=id,
        name=params['name'],
        birth_date=params['birth_date'],
        gender=params['gender'],
        breed=params['breed'],
        coat=params['coat'],
        purchase_donation=params['purchase_donation'],
        entry_date=params['entry_date'],
        assigned_location=params['assigned_location'],
        assigned_activities_ja=params['assigned_activities_ja'],
        trainer_ids=trainer_ids
    ):
        flash("Caballo actualizado con éxito.", "info")
        return redirect(url_for("horses.index"))
    else:
        flash("Caballo no encontrado.", "error")
        return redirect(url_for("horses.index"))


# delete horse
@bp.get("/<int:id>/delete")
@has_permission("horse_destroy")
def delete(id):
    """
    Elimina un caballo específico.
    
    :param id: ID del caballo a eliminar.
    """
    if horse_repository.delete_horse(id):
        flash("Caballo eliminado con éxito.", "info")
        return redirect(url_for("horses.index"))
    else:
        flash("Caballo no encontrado.", "error")
        return redirect(url_for("horses.index"))
