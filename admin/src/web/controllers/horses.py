from flask import Blueprint, redirect, render_template, request, url_for, flash
from src.core.models import horse
from src.core.models.employee import Employee
from src.core.repositories import horse as horse_repository
from src.core.repositories import document as document_repository
from src.core.repositories import employee as employee_repository
from src.web.helpers.auth import has_permission
from src.core.repositories.employee import get_employees_by_job_positions
from src.core.database import db


bp = Blueprint("horses", __name__, url_prefix="/horses")

#list horses
@bp.get("/")
@has_permission("horse_index") #permiso para listar caballos
def index():
    search = request.args.get("search", "")
    assigned_activities_ja = request.args.get("assigned_activities_ja", None)
    sort_by = request.args.get("sort_by", "name")
    direction = request.args.get("direction", "asc")
    page = int(request.args.get("page", 1))

    horses = horse_repository.list_horses(search, assigned_activities_ja, sort_by, direction, page)

    if not horses.items:
        flash("No se encontraron caballos.", "info")
    return render_template("horses/index.html", pagination=horses)

#register horse
@bp.get("/create")
@has_permission("horse_create")
def register():
    job_positions =["Conductor", "Entrenador de Caballos"]
    trainers = get_employees_by_job_positions(job_positions)
    return render_template("horses/form.html", is_update=False, title='Crear Caballo', trainers=trainers)

# Create horse
@bp.post("/create")
@has_permission("horse_create")
def create():
    params = request.form
    required_fields = [
        'name',
        'birth_date',
        'gender',
        'breed',
        'coat',
        'purchase_donation',
        'entry_date',
        'assigned_location',
        'assigned_activities_ja'
    ]
    for field in required_fields:
        if field not in params:
            flash(f"El campo {field} es requerido.", "error")
            return redirect(url_for("horses.register"))

    trainer_ids = request.form.getlist('trainer_id')

    horse = horse_repository.create_horse(
        name = params['name'],
        birth_date = params['birth_date']  or None,
        gender = params['gender'],
        breed = params['breed'],
        coat = params['coat'],
        purchase_donation = params['purchase_donation'],
        entry_date = params['entry_date'],
        assigned_location = params['assigned_location'],
        assigned_activities_ja = params['assigned_activities_ja'],
        trainer_ids=trainer_ids
    )
    flash("Caballo creado con éxito.", "success")
    return redirect(url_for("horses.index"))

# show horse
@bp.get("/<int:id>/show")
@has_permission("horse_show")
def show(id):
    horse = horse_repository.get_horse(id)
    if not horse:
        flash("Caballo no encontrado.", "error")
        return redirect(url_for("horses.index"))
    return render_template("horses/show.html", horse=horse)

# Edit horse
@bp.get("/<int:id>/update")
@has_permission("horse_update")
def edit(id):
    horse = horse_repository.get_horse(id)
    job_positions =["Conductor", "Entrenador de Caballos"]
    trainers = get_employees_by_job_positions(job_positions)
    associated_trainer_ids = [trainer.id for trainer in horse.association]
    if not horse:
        flash("Caballo no encontrado.", "error")
        return redirect(url_for("horses.index"))
    return render_template("horses/form.html", is_update=True, title='Editar Caballo', horse=horse, trainers=trainers,associated_trainer_ids=associated_trainer_ids)

#update horse
@bp.post("/<int:id>/update")
@has_permission("horse_update")
def update(id):

    params = request.form

    # Obtener los nuevos IDs de entrenadores seleccionados desde el formulario
    trainer_ids = request.form.getlist('trainer_id')


    if horse_repository.update_horse(
        horse_id=id,
        name = params['name'],
        birth_date = params['birth_date'],
        gender = params['gender'],
        breed = params['breed'],
        coat = params['coat'],
        purchase_donation = params['purchase_donation'],
        entry_date = params['entry_date'],
        assigned_location = params['assigned_location'],
        assigned_activities_ja = params['assigned_activities_ja'],
        trainer_ids=trainer_ids
        ):
        flash("Caballo actualizado con éxito.", "info")
        return redirect(url_for("horses.index"))
    else:
        flash("Caballo no encontrado.", "error")
        return redirect(url_for("horses.index"))


#delete horse
@bp.get("/<int:id>/delete")
@has_permission("horse_destroy")
def delete(id):
    if horse_repository.delete_horse(id):
        flash("Caballo eliminado con éxito.", "info")
        return redirect(url_for("horses.index"))
    else:
        flash("Caballo no encontrado.", "error")
        return redirect(url_for("horses.index"))
