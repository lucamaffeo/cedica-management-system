from flask import Blueprint, redirect, render_template, request, url_for, flash, current_app, session
from datetime import datetime
from src.core.repositories import user as user_repository, content as content_repository
from src.web.helpers.auth import has_permission

bp = Blueprint("contents", __name__, url_prefix="/contents")

def validate_content_form(params):
    title = params.get('title')
    summary = params.get('summary')
    content = params.get('content')
    status = params.get('status')
    if not title or not summary or not content or not status:
        flash("Todos los campos son obligatorios.", "error")
        return False
    return True

@bp.get("/")
@has_permission("content_index")
def index():
    search = request.args.get('search')
    status = request.args.get('status')
    sort_by = request.args.get('sort_by', 'title')
    direction = request.args.get('direction', 'asc')
    page = request.args.get('page', 1, type=int)
    contents = content_repository.list_contents(search, status, sort_by, direction, page)

    if not contents.items:
        flash("No se encontraron contenidos.", "info")
    return render_template("contents/index.html", pagination=contents)

@bp.get("/create")
@has_permission("content_create")
def register():
    return render_template("contents/form.html", is_update=False, title="Crear Contenido")

@bp.post("/create")
@has_permission("content_create")
def create():
    params = request.form
    if not validate_content_form(params):
        return redirect(url_for("contents.register"))

    content_repository.create_content(
        title=params.get('title'),
        summary=params.get('summary'),
        content=params.get('content'),
        author_id=session.get('user_id'),
        status=params.get('status')
    )

    flash("Contenido creado con éxito.", "info")
    return redirect(url_for("contents.index"))

@bp.get("/<int:id>/show")
@has_permission("content_show")
def show(id):
    content = content_repository.get_content(id)
    if not content:
        flash("Contenido no encontrado.", "error")
        return redirect(url_for("contents.index"))
    # Asegúrate de que las fechas no sean None
    content.update_date = content.update_date or datetime.min
    content.publication_date = content.publication_date or datetime.min
    return render_template("contents/show.html", content=content)

@bp.get("/<int:id>/update")
@has_permission("content_update")
def edit(id):
    content = content_repository.get_content(id)
    if not content:
        flash("Contenido no encontrado.", "error")
        return redirect(url_for("contents.index"))
    return render_template("contents/form.html", is_update=True, title="Editar Contenido", content=content)

@bp.route("/<int:id>/update", methods=["POST", "PATCH"])
@has_permission("content_update")
def update(id):
    params = request.form
    if not validate_content_form(params):
        return redirect(url_for("contents.edit", id=id))

    update_data = {
        'title': params.get('title'),
        'summary': params.get('summary'),
        'content': params.get('content'),
        'status': params.get('status'),
        'update_date': datetime.now()
    }
    if params.get('status') == 'Publicado':
        update_data['publication_date'] = datetime.now()

    content_repository.update_content(id, **update_data)

    flash("Contenido actualizado con éxito.", "info")
    return redirect(url_for("contents.index"))

@bp.get("/<int:id>/delete")
@has_permission("content_destroy")
def delete(id):
    if content_repository.delete_content(id):
        flash("Contenido eliminado con éxito.", "info")
    else:
        flash("Contenido no encontrado.", "error")
    return redirect(url_for("contents.index"))