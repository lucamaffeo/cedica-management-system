import re
from flask import Blueprint, redirect, render_template, request, url_for, flash
from src.core.repositories import employee as employee_repository
from src.core.repositories import user as user_repository
from src.web.helpers.auth import has_permission
from src.core.validation.models.employee import EmployeeValidator
from src.web.helpers.flash import flash_validation_errors


bp = Blueprint("employees", __name__, url_prefix="/employees")

# list employees


@bp.get("/")
@has_permission("employee_index")  # permiso para listar empleados
def index():
    """
    Renderiza la página de índice de empleados con paginación y filtros.
    """
    search = request.args.get("search", "")
    job_position_filter = request.args.get("job_position", None)
    sort_by = request.args.get("sort_by", "name")
    direction = request.args.get("direction", "asc")
    page = int(request.args.get("page", 1))

    employees = employee_repository.list_employees(
        search, job_position_filter, sort_by, direction, page)

    if not employees.items:
        flash("No se encontraron empleados.", "info")

    return render_template("employees/index.html", pagination=employees, job_position_filter=job_position_filter)


# Register
@bp.get("/create")
@has_permission("employee_create")
def register():
    """
    Renderiza el formulario para crear un nuevo empleado.
    """
    users = user_repository.list_unassociated_users()
    return render_template("employees/form.html", is_update=False, title='Crear Empleado', users=users)
    

# Create employee


@bp.post("/create")
@has_permission("employee_create")
def create():
    """
    Crea un nuevo empleado basado en los datos del formulario.
    """
    params = request.form.to_dict()

    validator = EmployeeValidator()
    errors = validator.validate_create(params)

    if errors:
        flash_validation_errors(errors)
        return redirect(url_for("employees.register"))

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
        user_id=params.get('user_id') or None,
    )

    flash("Empleado creado con éxito.", "info")
    return redirect(url_for("employees.index"))

# Show employee


@bp.get("/<int:id>/show")
@has_permission("employee_show")
def show(id):
    """
    Muestra los detalles de un empleado específico.
    
    :param id: ID del empleado a mostrar.
    """
    employee = employee_repository.get_employee(id)
    if not employee:
        flash("Empleado no encontrado.", "error")
        return redirect(url_for("employees.index"))
    return render_template("employees/show.html", employee=employee)

# Editar empleado


@bp.get("/<int:id>/update")
@has_permission("employee_update")
def edit(id):
    """
    Renderiza el formulario para editar un empleado existente.
    
    :param id: ID del empleado a editar.
    """
    employee = employee_repository.get_employee(id)
    if not employee:
        flash("Empleado no encontrado.", "error")
        return redirect(url_for("employees.index"))
    users = user_repository.list_unassociated_users()
    return render_template("employees/form.html", is_update=True, title='Actualizar Empleado', employee=employee, users=users)


@bp.post("/<int:id>/update")
@has_permission("employee_update")
def update(id):
    """
    Actualiza un empleado existente basado en los datos del formulario.
    
    :param id: ID del empleado a actualizar.
    """
    params = request.form.to_dict()

    validator = EmployeeValidator(id)
    errors = validator.validate_update(params)

    if errors:
        flash_validation_errors(errors)
        return redirect(url_for("employees.edit", id=id))

    # Obtener el empleado actual
    employee = employee_repository.get_employee(id)
    if not employee:
        flash("Empleado no encontrado.", "error")
        return redirect(url_for("employees.index"))

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
        termination_date=params.get("termination_date") or None,
        emergency_contact_info=params.get("emergency_contact_info"),
        social_work=params.get("social_work"),
        associate_number=employee.associate_number,
        condition=params.get("condition"),
        active='active' in params,
        user_id=params.get('user_id') or None,
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
    """
    Elimina un empleado específico.
    
    :param id: ID del empleado a eliminar.
    """
    if employee_repository.delete_employee(id):
        flash("Empleado eliminado con éxito.", "info")
        return redirect(url_for("employees.index"))
    else:
        flash("Empleado no encontrado.", "error")
        return redirect(url_for("employees.index"))
