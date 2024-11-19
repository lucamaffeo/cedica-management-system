import re
from flask import Blueprint, redirect, render_template, request, url_for, flash
from src.core.repositories import employee as employee_repository
from src.core.repositories import user as user_repository
from src.web.helpers.auth import has_permission
from werkzeug.utils import secure_filename
from os import fstat
from flask import current_app
from src.core.validation.models.employee import EmployeeValidator
from src.web.helpers.flash import flash_validation_errors


bp = Blueprint("employees", __name__, url_prefix="/employees")

#list employees
@bp.get("/")
@has_permission("employee_index") #permiso para listar empleados
def index():
    search = request.args.get("search", "")
    job_position_filter = request.args.get("job_position", None)
    sort_by = request.args.get("sort_by", "name")
    direction = request.args.get("direction", "asc")
    page = int(request.args.get("page", 1))

    employees = employee_repository.list_employees(search, job_position_filter, sort_by, direction, page)

    if not employees.items:
        flash("No se encontraron empleados.", "info")
    print("Job position filter:", job_position_filter)
    return render_template("employees/index.html", pagination=employees,job_position_filter=job_position_filter)


# Register
@bp.get("/create")
@has_permission("employee_create")
def register():
    users = user_repository.list_unassociated_users()
    return render_template("employees/form.html", is_update=False, title='Crear Empleado', users=users)

# Create employee
@bp.post("/create")
@has_permission("employee_create")
def create():
    params = request.form.to_dict()

    validator = EmployeeValidator()
    errors = validator.validate_create(params)

    if errors:
        flash_validation_errors(errors)
        return redirect(url_for("employees.register"))

    user_id = params.get('user_id')

    employee_repository.create_employee(
        name=params['name'],
        surname=params['surname'],
        dni=params['dni'],
        address=params['address'],
        email=params['email'],
        city=params['city'],
        telephone=params['telephone'],
        profession=params['profession'],
        job_position=params['job_position'],
        start_date=params['start_date'],
        termination_date=params.get('termination_date') or None,
        emergency_contact_info=params.get('emergency_contact_info'),
        social_work=params.get('social_work'),
        associate_number=params.get('associate_number'),
        condition=params['condition'],
        active=True,
        user_id=user_id,
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
    users = user_repository.list_unassociated_users()
    return render_template("employees/form.html", is_update=True, title='Actualizar Empleado', employee=employee, users=users)

@bp.post("/<int:id>/update")
@has_permission("employee_update")
def update(id):
    params = request.form.to_dict()

    validator = EmployeeValidator(id)
    errors = validator.validate_update(params)

    if errors:
        flash_validation_errors(errors)
        return redirect(url_for("employees.edit", id=id))

    termination_date = params.get("termination_date")
    if not termination_date:  # Si está vacío o None
        termination_date = None

    # Obtener el empleado actual
    employee = employee_repository.get_employee(id)
    if not employee:
        flash("Empleado no encontrado.", "error")
        return redirect(url_for("employees.index"))

    user_id = params.get('user_id')

    # Actualizar el empleado
    if employee_repository.update_employee(
        id=id,
        name=params.get("name"),
        surname=params.get("surname"),
        dni=employee.dni,
        address=params.get("address"),
        email=employee.email,
        city=params.get("city"),
        telephone=params.get("telephone"),
        profession=params.get("profession"),
        job_position=params.get("job_position"),
        start_date=params.get("start_date"),
        termination_date=termination_date,
        emergency_contact_info=params.get("emergency_contact_info"),
        social_work=params.get("social_work"),
        associate_number=employee.associate_number,
        condition=params.get("condition"),
        active='active' in params,
        user_id=user_id,
    ):
        flash("Empleado actualizado con éxito.", "success")
        return redirect(url_for("employees.index"))
    else:
        flash("Empleado no encontrado.", "error")
        return redirect(url_for("employees.index"))

# destroy employee
@bp.get("/<int:id>/delete")
@has_permission("employee_destroy")
def delete(id):
    if employee_repository.delete_employee(id):
        flash("Empleado eliminado con éxito.", "info")
        return redirect(url_for("employees.index"))
    else:
        flash("Empleado no encontrado.", "error")
        return redirect(url_for("employees.index"))
