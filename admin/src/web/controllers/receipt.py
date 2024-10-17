from datetime import datetime
from flask import Blueprint, flash, redirect, render_template, request, url_for
from src.core.repositories import receipt,employee as employee_repository
from src.web.helpers.auth import has_permission

bp = Blueprint("receipts", __name__, url_prefix="/receipts")

@bp.get("/")
@has_permission("receipt_index")
def index():
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    medio_pago = request.args.get('medio_pago')
    sort_by = request.args.get('sort_by', 'id')
    direction = request.args.get('direction', 'asc')
    page = request.args.get('page', 1, type=int)
    items_per_page = request.args.get('items_per_page', 5, type=int)
    
    receipts = receipt.list_receipts(start_date, end_date, medio_pago, sort_by, direction, page, items_per_page)
    
    return render_template("receipts/index.html", pagination=receipts)

@bp.get("/create")
@has_permission("receipt_create")
def register():
    employees = employee_repository.list_employees()
    ##riders = riders_repository.list_riders()
    return render_template("receipts/form.html", is_update=False, title="Registrar Recibo",employees=employees)##, riders=riders)

@bp.post("/create")
@has_permission("receipt_create")
def create():
    params = request.form
    empleado_id = params.get('empleado_id')
    ja_id = params.get('ja_id')

    if not empleado_id and not ja_id:
        flash("Debe seleccionar un empleado y J&A ", "error")
        return redirect(url_for("receipts.create"))
    monto = params.get('monto')
    if monto:
        monto = float(monto.replace('.', '').replace(',', '.'))

    # Aquí agregas la lógica para crear el recibo
    receipt.create_receipt(
        empleado_id=empleado_id,
        ja_id=1,
        fecha_pago=params['fecha_pago'] or None,
        monto=monto,
        medio_pago=params['medio_pago'],
        observaciones=params.get('observaciones'),
        al_dia=params.get('al_dia') == 'True'
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
    return render_template("receipts/form.html", is_update=True, title="Actualizar Recibo", receipt=r, employees=employees)# aqui tmb va el riders.

@bp.route("/<int:id>/update", methods=["POST", "PATCH"])
@has_permission("receipt_update")
def update(id):
    params = request.form
    empleado_id = params.get('empleado_id')
    ja_id = params.get('ja_id')
    monto = params.get('monto')
    if monto:
        monto = float(monto.replace('.', '').replace(',', '.'))

    if not empleado_id and not ja_id:
        flash("Debe seleccionar un empleado y J&A", "error")
        return redirect(url_for("receipts.create"))
    
    
    receipt.update_receipt(
        id=id,
        empleado_id=empleado_id,
        ja_id=ja_id,
        fecha_pago=params['fecha_pago'] or None,
        monto=monto,
        medio_pago=params['medio_pago'],
        observaciones=params.get('observaciones'),
        al_dia=params.get('al_dia') == 'True'
    )
    
    flash("Recibo actualizado con éxito.", "success")
    return redirect(url_for("receipts.index"))

@bp.get("/<int:id>/delete")
@has_permission("receipt_destroy")
def delete(id):
    r = receipt.get_receipt(id)
    if not r:
        flash("Recibo no encontrado.", "error")
        return redirect(url_for("receipts.index"))

    receipt.delete_receipt(id)
    flash("Recibo eliminado con éxito.", "info")
    return redirect(url_for("receipts.index"))