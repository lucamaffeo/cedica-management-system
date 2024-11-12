from flask import Blueprint, redirect, render_template, request, url_for, flash, current_app, session
from datetime import datetime
from src.core.repositories import user as user_repository, content as content_repository
from src.web.helpers.auth import has_permission
from src.core.validation.models.content import ContentValidator

bp = Blueprint("contents", __name__, url_prefix="/contents")

@bp.get("/")
@has_permission("content_index")
def index():
    search = request.args.get('search')
    status_id = request.args.get('status', None, type=int)
    sort_by = request.args.get('sort_by', 'title')
    direction = request.args.get('direction', 'asc')
    page = request.args.get('page', 1, type=int)
    contents = content_repository.list_contents(search, status_id, sort_by, direction, page)

    if not contents.items:
        flash("No se encontraron contenidos.", "info")
    return render_template("contents/index.html", pagination=contents)

@bp.get("/create")
@has_permission("content_create")
def register():
    return render_template("contents/form.html", is_update=False, title="Crear Contenido", statuses=content_repository.list_statuses())

@bp.post("/create")
@has_permission("content_create")
def create():
    params = request.form.to_dict()
    validator = ContentValidator()
    errors = validator.validate_for_create(params)
    if errors:
        for error in errors:
            flash(f"{error.field}: {error.message}", "error")
        return redirect(url_for("contents.register"))

    content_repository.create_content(
        title=params.get('title'),
        summary=params.get('summary'),
        content=params.get('content'),
        author_id=session.get('user_id'),
        status_id=params.get('status')
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

    return render_template("contents/show.html", content=content)

@bp.get("/<int:id>/update")
@has_permission("content_update")
def edit(id):
    content = content_repository.get_content(id)
    if not content:
        flash("Contenido no encontrado.", "error")
        return redirect(url_for("contents.index"))
    return render_template("contents/form.html", is_update=True, title="Editar Contenido", content=content, statuses=content_repository.list_statuses())

@bp.route("/<int:id>/update", methods=["POST", "PATCH"])
@has_permission("content_update")
def update(id):
    params = request.form.to_dict()
    validator = ContentValidator(content_id=id)
    errors = validator.validate_for_update(params)
    if errors:
        for error in errors:
            flash(f"{error.field}: {error.message}", "error")
        return redirect(url_for("contents.edit", id=id))
    
    content = content_repository.get_content(id)
    update_data = {
        'title': params.get('title'),
        'summary': params.get('summary'),
        'content': params.get('content'),
        'update_date': datetime.now()
    }

    if params.get('status'):
        update_data['status_id'] = params.get('status')
        if params.get('status') == '2': 
            update_data['publication_date'] = datetime.now()
    else:
        update_data['status_id'] = content.status_id

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