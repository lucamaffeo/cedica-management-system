from flask import Blueprint, flash, redirect, render_template, request, url_for
from src.core.repositories import receipt
from src.web.helpers.auth import has_permission
from src.core.repositories import receipt

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
    items_per_page = 5
    
    receipts = receipt.list_receipts(start_date, end_date, medio_pago, sort_by, direction, page, items_per_page)
    
    return render_template("receipts/index.html", pagination=receipts)

@bp.get("/create")
@has_permission("receipt_create")
def register():
    return render_template("receipts/form.html", is_update=False, title="Registrar Recibo")

@bp.post("/create")
@has_permission("receipt_create")
def create():
    params = request.form
    required_fields = ['fecha_pago', 'monto', 'medio_pago', 'observaciones']
    for field in required_fields:
        if field not in params:
            flash(f"El campo {field} es requerido.", "error")
            return redirect(url_for("receipts.register"))
    receipt.create_receipt(
        fecha_pago=params['fecha_pago'],
        monto=params['monto'],
        medio_pago=params['medio_pago'],
        observaciones=params['observaciones']
    )


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
    return render_template("receipts/form.html", is_update=True, title="Actualizar Recibo", receipt=r)

@bp.route("/<int:id>/update", methods=["POST", "PATCH"])
@has_permission("receipt_update")
def update(id):
    params = request.form
    try:
        r = receipt.update_receipt(id, **params)
    except ValueError as e:
        flash(str(e), 'error')
        return redirect(url_for("receipts.index"))
    return redirect(url_for("receipts.index"))

@bp.get("/<int:id>/delete")
@has_permission("receipt_destroy")
def delete(id):
    r = receipt.get_receipt(id)
    if not r:
        flash("Recibo no encontrado.", "error")
        return redirect(url_for("receipts.index"))

    receipt.delete_receipt(id)
    flash("Recibo eliminado con Ã©xito.", "info")
    return redirect(url_for("receipts.index"))