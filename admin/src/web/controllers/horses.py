from flask import Blueprint, redirect, render_template, request, url_for, flash
from src.core.repositories import horse as horse_repository
from src.web.helpers.auth import has_permission


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
    items_per_page = 5

    horses = horse_repository.list_horses(search, assigned_activities_ja, sort_by, direction, page, items_per_page)    

    if not horses.items:
        flash("No se encontraron caballos.", "info")
    return render_template("horses/index.html", pagination=horses)

#register horse
@bp.get("/create")
@has_permission("horse_create")
def register():
    return render_template("horses/form.html", is_update=False, title='Crear Caballo')

# Create horse
@bp.post("/create")
@has_permission("horse_create")
def create():
    params = request.form
    required_fields = [
        'id',
        'name',
        'birth_date',
        'gender',
        'breed',
        'coat',
        'purchase_donation',
        'entry_date',
        'assigned_location',
        'trainer_id',
        'assigned_activities_ja'
    ]
    for field in required_fields:
        if field not in params:
            flash(f"El campo {field} es requerido.", "error")
            return redirect(url_for("horses.register"))
    horse_repository.create_horse(
        id = params['id'],
        name = params['name'],
        birth_date = params['birth_date'],
        gender = params['gender'],
        breed = params['breed'],
        coat = params['coat'],
        purchase_donation = params['purchase_donation'],
        entry_date = params['entry_date'],
        assigned_location = params['assigned_location'],
        trainer_id = params['trainer_id'],
        assigned_activities_ja = params['assigned_activities_ja'],
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
    if not horse:
        flash("Caballo no encontrado.", "error")
        return redirect(url_for("horses.index"))
    return render_template("horses/form.html", is_update=True, title='Editar Caballo', horse=horse)

#update horse
@bp.post("/<int:id>/update")
@has_permission("horse_update")
def update(id):
    horse = horse_repository.get_horse(id)
    if not horse:
        flash("Caballo no encontrado.", "error")
        return redirect(url_for("horses.index"))
    
    params = request.form

    horse_repository.update_horse(
        id=id,
        name = params['name'],
        birth_date = params['birth_date'],
        gender = params['gender'],
        breed = params['breed'],
        coat = params['coat'],
        purchase_donation = params['purchase_donation'],
        entry_date = params['entry_date'],
        assigned_location = params['assigned_location'],
        trainer_id = params['trainer_id'],
        assigned_activities_ja = params['assigned_activities_ja'],
    )
    flash("Caballo actualizado con éxito.", "info")
    return redirect(url_for("horses.index"))

#delete horse
@bp.get("/<int:id>/delete")
@has_permission("horse_delete")
def delete(id):
    horse = horse_repository.get_horse(id)
    if not horse:
        flash("Caballo no encontrado.", "error")
        return redirect(url_for("horses.index"))
    horse_repository.delete_horse(id)
    flash("Caballo eliminado con éxito.", "info")
    return redirect(url_for("horses.index"))