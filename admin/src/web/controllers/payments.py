from flask import Blueprint, flash, redirect, render_template, request, url_for
from src.core.repositories import payment
from src.web.helpers.auth import has_permission

bp = Blueprint("payments", __name__, url_prefix="/payments")

@bp.get("/")
@has_permission("payment_index")
def index():

    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    payment_type = request.args.get('type')
    sort_by = request.args.get('sort_by', 'date')
    direction = request.args.get('direction', 'asc')
    page = request.args.get('page', 1, type=int)
    
    payments = payment.list_payments(start_date, end_date, payment_type, sort_by, direction, page)

    return render_template("payments/index.html", pagination=payments)

@bp.get("/create")
@has_permission("payment_create")
def register():
    return render_template("payments/form.html", is_update=False, title="Registrar Pago")

@bp.post("/create")
@has_permission("payment_create")
def create():
    params = request.form
    try:
        p = payment.create_payment(**params)
    except ValueError as e:
        flash(str(e), 'error')
        return redirect(url_for('payments.register'))
    return redirect(url_for('payments.index'))

@bp.get("/<int:id>/show")
@has_permission("payment_show")
def show(id):
    p = payment.get_payment(id)
    if not p:
        flash("Pago no encontrado.", "error")
        return redirect(url_for("payments.index"))
    return render_template("payments/show.html", payment=p)

@bp.get("/<int:id>/update")
@has_permission("payment_update")
def edit(id):
    p = payment.get_payment(id)
    if not p:
        flash("Pago no encontrado.", "error")
        return redirect(url_for("payments.index"))
    return render_template("payments/form.html", is_update=True, title="Actualizar Pago", payment=p)

@bp.route("/<int:id>/update", methods=["POST", "PATCH"])
@has_permission("payment_update")
def update(id):
    params = request.form
    try:
        p = payment.update_payment(id, **params)
    except ValueError as e:
        flash(str(e), 'error')
        return redirect(url_for("payments.index"))
    return redirect(url_for("payments.index"))

@bp.get("/<int:id>/delete")
@has_permission("payment_destroy")
def delete(id):
    p = payment.get_payment(id)
    if not p:
        flash("Pago no encontrado.", "error")
        return redirect(url_for("payments.index"))

    payment.delete_payment(id)
    flash("Pago eliminado con éxito.", "info")
    return redirect(url_for("payments.index"))
