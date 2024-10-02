from flask import Blueprint, redirect, render_template, request, session, url_for, flash
from src.core.repositories import employee as employee_repository
from src.web.helpers.auth import has_permission

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
    return render_template("employees/index.html", employees=employees)


# Register
@bp.get("/register")
@has_permission("employee_create")
def register():
    return render_template("users/form.html", is_update=False, title='Crear Empleado')

# Create employee
@bp.post("/register")
@has_permission("employee_create")
def create():
    params = request.form
    required_fields = ['name', 'surname', 'dni', 'address', 'email', 'city', 'telephone',
                       'profession', 'job_position', 'start_date','emergency_contact_info=emergency_contact_info',
                       'condition']
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
        active = params.get('active', False),
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
    #is_update_own = id == session["user"]["id"]
                                                                    
  #  if not is_update_own:
   #     has_permission("user_update")(lambda: None)() # estas 3 no se si van, supongo q si

    employee = employee_repository.get_employee(id)
    if not employee:
        flash("Empleado no encontrado.", "error")
        return redirect(url_for("employees.index"))

    params = request.form
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
        termination_date=params.get("termination_date"),
        emergency_contact_info=params.get("emergency_contact_info"),
        social_work=params.get("social_work"),
        associate_number=params.get("associate_number"),
        condition=params.get("condition"),
        active=params.get("active"),
    )

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