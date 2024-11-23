from flask import Blueprint, flash, redirect, render_template, request, url_for
from src.core.repositories import payment
from src.core.repositories import employee as employee_repository
from src.core.validation.models.payment import PaymentValidator
from src.web.helpers.auth import has_permission
from src.web.helpers.flash import flash_validation_errors

bp = Blueprint("payments", __name__, url_prefix="/payments")


@bp.get("/")
@has_permission("payment_index")
def index():
    """
    Renderiza la página de índice de pagos con paginación y filtros.
    """
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    payment_type = request.args.get('type')
    sort_by = request.args.get('sort_by', 'date')
    direction = request.args.get('direction', 'asc')
    page = request.args.get('page', 1, type=int)

    payments = payment.list_payments(
        start_date, end_date, payment_type, sort_by, direction, page)

    beneficiaries = employee_repository.get_all()

    payment_types = payment.get_payment_types()

    return render_template("payments/index.html", pagination=payments, beneficiaries=beneficiaries, payment_types=payment_types)


@bp.get("/create")
@has_permission("payment_create")
def register():
    """
    Renderiza el formulario para crear un nuevo pago.
    """
    employees = employee_repository.get_all()
    payment_types = payment.get_payment_types()
    return render_template("payments/form.html", is_update=False, title="Registrar Pago", employees=employees, payment_types=payment_types)


@bp.post("/create")
@has_permission("payment_create")
def create():
    """
    Crea un nuevo pago basado en los datos del formulario.
    """
    params = request.form.to_dict()

    validator = PaymentValidator()
    errors = validator.validate_create(params)

    if errors:
        flash_validation_errors(errors)
        return redirect(url_for('payments.register'))

    try:
        p = payment.create_payment(**params)
        flash("Pago registrado con éxito.", "success")
    except ValueError as e:
        flash(str(e), 'error')
        return redirect(url_for('payments.register'))

    return redirect(url_for('payments.index'))


@bp.get("/<int:id>/show")
@has_permission("payment_show")
def show(id):
    """
    Muestra los detalles de un pago específico.
    
    :param id: ID del pago a mostrar.
    """
    p = payment.get_payment(id)
    if not p:
        flash("Pago no encontrado.", "error")
        return redirect(url_for("payments.index"))
    return render_template("payments/show.html", payment=p)


@bp.get("/<int:id>/update")
@has_permission("payment_update")
def edit(id):
    """
    Renderiza el formulario para editar un pago existente.
    
    :param id: ID del pago a editar.
    """
    p = payment.get_payment(id)
    if not p:
        flash("Pago no encontrado.", "error")
        return redirect(url_for("payments.index"))
    employees = employee_repository.get_all()
    payment_types = payment.get_payment_types()

    return render_template("payments/form.html", is_update=True, title="Actualizar Pago", payment=p, employees=employees, payment_types=payment_types)


@bp.route("/<int:id>/update", methods=["POST", "PATCH"])
@has_permission("payment_update")
def update(id):
    """
    Actualiza un pago existente basado en los datos del formulario.
    
    :param id: ID del pago a actualizar.
    """
    params = request.form.to_dict()

    validator = PaymentValidator()
    errors = validator.validate_update(params, id)

    if errors:
        flash_validation_errors(errors)
        return redirect(url_for("payments.edit", id=id))

    try:
        p = payment.update_payment(id, **params)
        flash("Pago actualizado con éxito.", "success")
    except ValueError as e:
        flash(str(e), 'error')
        return redirect(url_for("payments.edit", id=id))

    return redirect(url_for("payments.index"))


@bp.get("/<int:id>/delete")
@has_permission("payment_destroy")
def delete(id):
    """
    Elimina un pago específico.
    
    :param id: ID del pago a eliminar.
    """
    if payment.delete_payment(id):
        flash("Pago eliminado con éxito.", "info")
        return redirect(url_for("payments.index"))
    else:
        flash("Pago no encontrado.", "error")
        return redirect(url_for("payments.index"))
