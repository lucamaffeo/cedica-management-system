from flask import Blueprint, redirect, render_template, request, session, url_for, flash
from src.core.repositories import riders as rider_repository
from src.web.helpers.auth import has_permission
from werkzeug.utils import secure_filename
from os import fstat
from flask import current_app


bp = Blueprint("riders", __name__, url_prefix="/riders")

#list riders
@bp.get("/")
@has_permission("rider_index") #permiso para listar jinetes y amazonas
def index():
    search = request.args.get("search", "")
    sort_by = request.args.get("sort_by", "nombre")
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
    return render_template("riders/form.html", is_update=False, title='Crear Jinete/Amazona')

# Create rider
@bp.post("/create")
@has_permission("rider_create")
def create():
    becado = 'becado' in request.form
    params = request.form
    required_fields = ['nombre', 'apellido', 'dni', 'edad', 'fecha_nacimiento', 'lugar_nacimiento', 'domicilio',
                       'telefono', 'contacto_emergencia', 'tel_contacto','becado', 'porcentaje_beca', 'profesionales'
                       ]
    for field in required_fields:
        if field not in params:
            flash(f"El campo {field} es requerido.", "error")
            return redirect(url_for("riders.register"))
        
    rider_repository.create_rider(
        nombre = params['nombre'],
        apellido = params['apellido'],
        dni = params['dni'],
        edad = params['edad'],
        fecha_nacimiento = params['fecha_nacimiento'],
        lugar_nacimiento = params['lugar_nacimiento'],
        domicilio = params['domicilio'],
        telefono = params['telefono'],
        contacto_emergencia = params['contacto_emergencia'],
        tel_contacto = params['tel_contacto'],
        becado = becado,
        porcentaje_beca = params['porcentaje_beca'],
        profesionales = params['profesionales'],
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
    return render_template("riders/show.html", rider=rider)

# Editar jinete/amazona
@bp.get("/<int:id>/update")
@has_permission("rider_update")
def edit(id):
    rider = rider_repository.get_rider(id)
    if not rider:
        flash("Jinete/Amazona no encontrado.", "error")
        return redirect(url_for("riders.index"))
    return render_template("riders/form.html", is_update=True, title='Actualizar Jinete/Amazona', rider=rider)

@bp.post("/<int:id>/update")
@has_permission("rider_update")
def update(id):
    
    rider = rider_repository.get_rider(id)
    if not rider:
        flash("Jinete/Amazona no encontrado.", "error")
        return redirect(url_for("riders.index"))

    params = request.form    
    becado = 'becado' in request.form
    # Actualizar el jinete
    rider_repository.update_rider(
        id=id,
        nombre=params.get("nombre"),
        apellido=params.get("apellido"),
        dni=params.get("dni"),
        edad=params.get("edad"),
        fecha_nacimiento=params.get("fecha_nacimiento"),
        lugar_nacimiento=params.get("lugar_nacimiento"),
        domicilio=params.get("domicilio"),
        telefono=params.get("telefono"),
        contacto_emergencia=params.get("contacto_emergencia"),
        tel_contacto=params.get("tel_contacto"),
        becado=becado,
        porcentaje_beca=params.get("porcentaje_beca"),
        profesionales=params.get("profesionales")
    )
    # Manejar la carga de archivos

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