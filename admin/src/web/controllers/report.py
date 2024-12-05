from datetime import datetime
from src.core.validation.models.report import ReportValidator
from src.web.helpers.flash import flash_validation_errors
from src.core.models.horse import has_permission
from src.core.repositories.report import list_employees_by_seniority, list_receipts_by_payment_method, list_riders_by_age
from src.core.models import grafic
from src.core.repositories.grafic import generar_grafico_barras_apiladas_ingresos, generar_grafico_barras_becados, generar_grafico_barras_ingresos_por_mes, generar_grafico_torta_discapacidades
from src.core.database import db
from flask import url_for, render_template, request, send_file, Blueprint, redirect
from src.web.helpers.auth import has_permission


bp = Blueprint('report', __name__, url_prefix='/report')


@bp.route('/report/historial_cobros', methods=['GET'])
@bp.route('/')
@has_permission('report_index')
def index():
    """
    Renderiza la página principal de reportes.
    """
    return render_template('report/index.html')


@bp.route('/ingresos')
@has_permission('grafic_show')
def ingresos():
    """
    Genera y envía un gráfico de barras de ingresos por mes.
    """
    img = generar_grafico_barras_ingresos_por_mes()
    return send_file(img, mimetype='image/png')


@bp.route('/discapacidades')
@has_permission('grafic_show')
def discapacidades():
    """
    Genera y envía un gráfico de torta de discapacidades.
    """
    img = generar_grafico_torta_discapacidades()
    return send_file(img, mimetype='image/png')


@bp.route('/generate', methods=['GET'])
@has_permission('report_index')
def report_form():
    """
    Renderiza el formulario para generar reportes.
    """
    return render_template('report/reports_form.html')


@bp.route('/becados')
@has_permission('grafic_show')
def becados():
    """
    Genera y envía un gráfico de barras de becados.
    """
    img = generar_grafico_barras_becados()
    return send_file(img, mimetype='image/png')


@bp.route('/ingresos_apilados')
@has_permission('grafic_show')
def ingresos_apilados():
    """
    Genera y envía un gráfico de barras apiladas de ingresos.
    """
    img = generar_grafico_barras_apiladas_ingresos()
    return send_file(img, mimetype='image/png')


@bp.route('/antiguedad_empleados', methods=['GET'])
@has_permission('report_show')
def employee_seniority():
    """
    Genera un reporte de antigüedad de empleados con filtros y paginación.
    """
    sort_by = request.args.get("sort_by", "start_date")
    direction = request.args.get("direction", "asc")
    search = request.args.get('search')
    job_position = request.args.get('job_position')
    min_seniority = request.args.get('min_seniority', type=int)
    max_seniority = request.args.get('max_seniority', type=int)
    start_date = request.args.get('start_date', type=str)
    page = request.args.get('page', 1, type=int)

    # Convierte la fecha si está presente
    if start_date:
        start_date = datetime.strptime(start_date, "%Y-%m-%d")

    validators = ReportValidator()
    errors = validators.validate_AntiguedadEmpleados(request.args)
    if errors:
        flash_validation_errors(errors)
        return redirect(url_for("report.employee_seniority"))

    # Obtener empleados con paginación
    employees_pagination = list_employees_by_seniority(
        sort_by=sort_by,
        direction=direction,
        search=search,
        job_position=job_position,
        min_seniority=min_seniority,
        max_seniority=max_seniority,
        start_date=start_date,
        page=page
    )

    now = datetime.now()
    return render_template("report/employee_report.html", employees=employees_pagination, now=now, sort_by=sort_by, direction=direction)


@bp.route("/receipt_payment_method_report", methods=['GET'])
@has_permission('report_show')
def receipt_payment_method_report():
    """
    Genera un reporte de recibos por método de pago con filtros y paginación.
    """
    payment_method = request.args.get(
        'payment_method')  # Obtén el método de pago
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    sort_by = request.args.get('sort_by', 'payment_method')
    direction = request.args.get('direction', 'asc')
    min_receipts = request.args.get('min_receipts', type=int)
    max_receipts = request.args.get('max_receipts', type=int)
    min_quantity = request.args.get('min_quantity', type=int)
    max_quantity = request.args.get('max_quantity', type=int)
    page = request.args.get('page', 1, type=int)

    validators = ReportValidator()
    errors = validators.validate_receipt_payment_method_report(request.args)
    if errors:
        flash_validation_errors(errors)
        return redirect(url_for("report.receipt_payment_method_report"))

    report_data = list_receipts_by_payment_method(
        payment_method=payment_method,
        start_date=start_date,
        end_date=end_date,
        sort_by=sort_by,
        direction=direction,
        min_receipts=min_receipts,
        max_receipts=max_receipts,
        min_quantity=min_quantity,
        max_quantity=max_quantity,
        page=page
    )

    return render_template("report/receipt_report.html",
                           report_data=report_data.items,
                           pagination=report_data,
                           sort_by=sort_by, direction=direction)


@bp.route('/riders_by_age', methods=['GET'])
@has_permission('report_show')
def riders_by_age():
    """
    Genera un reporte de jinetes por edad con filtros y paginación.
    """
    direction = request.args.get("direction", "asc")
    sort_by = request.args.get("sort_by", "age")

    # Obtener los filtros de los parámetros de la URL
    name = request.args.get("name")
    surname = request.args.get("surname")
    dni = request.args.get("dni")
    min_age = request.args.get("min_age", type=int)
    max_age = request.args.get("max_age", type=int)
    page = request.args.get('page', 1, type=int)  # Obtener el número de página

    validators = ReportValidator()
    errors = validators.validate_riders_by_age(request.args)
    if errors:
        flash_validation_errors(errors)
        return redirect(url_for("report.riders_by_age"))

    # Obtener la lista de jinetes/amazonas con los filtros y ordenación aplicados
    riders = list_riders_by_age(
        sort_by=sort_by,
        direction=direction,
        name=name,
        surname=surname,
        dni=dni,
        min_age=min_age,
        max_age=max_age,
        page=page
    )

    return render_template("report/rider_report.html",
                           riders=riders.items,
                           pagination=riders,
                           sort_by=sort_by,
                           direction=direction)
