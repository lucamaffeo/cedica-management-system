from datetime import datetime
from flask import Blueprint, flash, redirect, render_template, request, url_for
from src.core.models.employee import Employee
from src.core.repositories import receipt, employee as employee_repository, riders as riders_repository
from src.web.helpers.auth import has_permission
from src.core.validation.models.receipt import ReceiptValidator

bp = Blueprint("receipts", __name__, url_prefix="/receipts")


@bp.get("/")
@has_permission("receipt_index")
def index():
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    payment_method = request.args.get('payment_method')
    sort_by = request.args.get('sort_by', 'id')
    direction = request.args.get('direction', 'asc')
    page = request.args.get('page', 1, type=int)

    receipts = receipt.list_receipts(
        start_date, end_date, payment_method, sort_by, direction, page)
    received_by = Employee.query.all()
    return render_template("receipts/index.html", pagination=receipts, received_by=received_by)


@bp.get("/create")
@has_permission("receipt_create")
def register():
    employees = employee_repository.list_employees()
    riders = riders_repository.list_riders()
    current_date = datetime.now().strftime('%Y-%m-%d')
    return render_template("receipts/form.html", is_update=False, title="Registrar Recibo", employees=employees, riders=riders, current_date=current_date)


@bp.post("/create")
@has_permission("receipt_create")
def create():
    params = request.form
    validator = ReceiptValidator()
    errors = validator.validate_create(params)

    if errors:
        for error in errors:
            flash(f"{error.field}: {error.message}", "error")
        return redirect(url_for("receipts.create"))

    receipt.create_receipt(
        employee_id=params.get('employee_id'),
        ja_id=params.get('ja_id'),
        payment_date=params['payment_date'] or None,
        quantity=params.get('quantity'),
        payment_method=params['payment_method'],
        remarks=params.get('remarks'),
        up_to_date=True,

    )

    flash("Recibo creado con éxito.", "info")
    return redirect(url_for("receipts.index"))


@bp.get("/<int:id>/show")
@has_permission("receipt_show")
def show(id):
    r = receipt.get_receipt(id)
    if not r:
        flash("Recibo no encontrado.", "error")
        return redirect(url_for("receipts.index"))
    return render_template("receipts/show.html", receipt=r)


@bp.get("/<int:id>/update")
@has_permission("receipt_update")
def edit(id):
    r = receipt.get_receipt(id)
    if not r:
        flash("Recibo no encontrado.", "error")
        return redirect(url_for("receipts.index"))
    employees = employee_repository.list_employees()
    riders = riders_repository.list_riders()
    current_date = datetime.now().strftime('%Y-%m-%d')
    return render_template("receipts/form.html", is_update=True, title="Actualizar Recibo", receipt=r, employees=employees, riders=riders, current_date=current_date)


@bp.route("/<int:id>/update", methods=["POST", "PATCH"])
@has_permission("receipt_update")
def update(id):
    params = request.form
    validator = ReceiptValidator()
    errors = validator.validate_update(params, id)

    if errors:
        for error in errors:
            flash(f"{error.field}: {error.message}", "error")
        return redirect(url_for('receipts.update', id=id))

    # Obtener el recibo
    receipt_obj = receipt.get_receipt(id)
    if not receipt_obj:
        flash("Recibo no encontrado.", "error")
        return redirect(url_for("receipts.index"))

    # Actualizar el recibo pasando el objeto
    receipt.update_receipt(
        receipt_obj,
        employee_id=params.get('employee_id'),
        ja_id=params.get('ja_id'),
        payment_date=params['payment_date'] or None,
        quantity=params.get('quantity'),
        payment_method=params['payment_method'],
        remarks=params.get('remarks') or None,
        up_to_date=params.get('up_to_date') == "on",
    )

    flash("Recibo actualizado con éxito.", "success")
    return redirect(url_for("receipts.index"))


@bp.get("/<int:id>/delete")
@has_permission("receipt_destroy")
def delete(id):
    # Obtener el recibo una sola vez
    receipt_obj = receipt.get_receipt(id)
    if not receipt_obj:
        flash("Recibo no encontrado.", "error")
        return redirect(url_for("receipts.index"))

    # Eliminar el recibo pasando el objeto obtenido
    receipt.delete_receipt(receipt_obj)
    flash("Recibo eliminado con éxito.", "info")
    return redirect(url_for("receipts.index"))

