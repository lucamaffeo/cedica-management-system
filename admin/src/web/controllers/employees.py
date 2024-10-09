from flask import Blueprint, redirect, render_template, request, url_for, flash
from src.core.repositories import employee as employee_repository
from src.web.helpers.auth import has_permission
from werkzeug.utils import secure_filename
from os import fstat
from flask import current_app


bp = Blueprint("employees", __name__, url_prefix="/employees")

#list employees
@bp.get("/")
@has_permission("employee_index") #permiso para listar empleados
def index():
    search = request.args.get("search", "")
    profession_filter = request.args.get("profession", None)
    sort_by = request.args.get("sort_by", "name")
    direction = request.args.get("direction", "asc")
    page = int(request.args.get("page", 1))
    items_per_page = 5

    employees = employee_repository.list_employees(search, profession_filter, sort_by, direction, page, items_per_page)    

    if not employees.items:
        flash("No se encontraron empleados.", "info")
    return render_template("employees/index.html", pagination=employees)


# Register
@bp.get("/create")
@has_permission("employee_create")
def register():
    return render_template("employees/form.html", is_update=False, title='Crear Empleado')

# Create employee
@bp.post("/create")
@has_permission("employee_create")
def create():
    params = request.form
    required_fields = ['name', 'surname', 'dni', 'address', 'email', 'city', 'telephone',
                       'profession', 'job_position', 'start_date','emergency_contact_info', 'social_work', 'associate_number',
                       'condition', 'termination_date']
    for field in required_fields:
        if field not in params:
            flash(f"El campo {field} es requerido.", "error")
            return redirect(url_for("employees.register"))
        
    employee_repository.create_employee(
        name = params['name'],
        surname = params['surname'],
        dni = params['dni'],
        address = params['address'],
        email = params['email'],
        city = params['city'],
        telephone = params['telephone'],
        profession = params['profession'],
        job_position = params['job_position'],
        start_date = params['start_date'],
        termination_date = params.get('termination_date'),
        emergency_contact_info= params.get('emergency_contact_info'),
        social_work = params.get('social_work'),
        associate_number = params.get('associate_number'),
        condition = params['condition'],
        active = True,
    )

    flash("Empleado creado con éxito.", "info")
    return redirect(url_for("employees.index"))

# Show employee
@bp.get("/<int:id>/show")
@has_permission("employee_show")
def show(id):
    employee = employee_repository.get_employee(id)
    if not employee:
        flash("Empleado no encontrado.", "error")
        return redirect(url_for("employees.index"))
    return render_template("employees/show.html", employee=employee)

# Editar empleado
@bp.get("/<int:id>/update")
@has_permission("employee_update")
def edit(id):
    employee = employee_repository.get_employee(id)
    if not employee:
        flash("Empleado no encontrado.", "error")
        return redirect(url_for("employees.index"))
    return render_template("employees/form.html", is_update=True, title='Actualizar Empleado', employee=employee)

@bp.post("/<int:id>/update")
@has_permission("employee_update")
def update(id):
    
    employee = employee_repository.get_employee(id)
    if not employee:
        flash("Empleado no encontrado.", "error")
        return redirect(url_for("employees.index"))

    params = request.form
    termination_date = params.get("termination_date")
    if not termination_date:  # Si está vacío o None
        termination_date = None
    # Actualizar el empleado
    employee_repository.update_employee(
        id=id,
        name=params.get("name"),
        surname=params.get("surname"),
        dni=params.get("dni"),
        address=params.get("address"),
        email=params.get("email"),
        city=params.get("city"),
        telephone=params.get("telephone"),
        profession=params.get("profession"),
        job_position=params.get("job_position"),
        start_date=params.get("start_date"),
        termination_date=termination_date,
        emergency_contact_info=params.get("emergency_contact_info"),
        social_work=params.get("social_work"),
        associate_number=params.get("associate_number"),
        condition=params.get("condition"),
        active= 'active' in params

    )
    # Manejar la carga de archivos
    files_to_upload = {
        'dni_copy': 'Copia DNI',
        'cv': 'CV Actualizado',
        'title': 'Título'
    }

    client = current_app.storage.client

    for field, doc_type in files_to_upload.items():
        if field in request.files:
            file = request.files[field]
            if file and file.filename:
                # Asegurarse de que el nombre del archivo sea seguro
                filename = secure_filename(file.filename)
                size = fstat(file.fileno()).st_size
                client.put_object(
                    "grupo10",  # Nombre del bucket
                    filename,  # Nombre del archivo en Minio
                    file,  # El archivo que se va a subir
                    size,  # Tamaño del archivo
                    content_type=file.content_type  # Tipo de contenido
                )
                flash(f"{doc_type} subido exitosamente.", "success")

    flash("Empleado actualizado con éxito.", "success")
    return redirect(url_for("employees.index"))

# destroy employee
@bp.get("/<int:id>/delete")
@has_permission("employee_destroy")
def delete(id):
    employee = employee_repository.get_employee(id)
    if not employee:
        flash("Empleado no encontrado.", "error")
        return redirect(url_for("employees.index"))

    employee_repository.delete_employee(id)
    flash("Empleado eliminado con éxito.", "info")
    return redirect(url_for("employees.index"))