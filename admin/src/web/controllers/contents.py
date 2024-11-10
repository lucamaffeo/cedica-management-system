from flask import Blueprint, redirect, render_template, request, url_for, flash
from src.core.repositories import user as user_repository
from src.core.repositories import content as content_repository
from src.web.helpers.auth import has_permission
from flask import current_app, session
from datetime import datetime


bp = Blueprint("contents", __name__, url_prefix="/contents")

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
    title = params.get('title')
    summary = params.get('summary')
    content = params.get('content')
    author_id = session.get('user_id')
    status = params.get('status')

    if not title or not summary or not content or not status:
        flash("Todos los campos son obligatorios.", "error")
        return redirect(url_for("contents.register"))

    content_repository.create_content(
        title=title,
        summary=summary,
        content=content,
        author_id=author_id,
        status=status
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
    return render_template("contents/form.html", is_update=True, title="Editar Contenido", content=content)

@bp.route("/<int:id>/update", methods=["POST", "PATCH"])
@has_permission("content_update")
def update(id):
    params = request.form
    title = params.get('title')
    summary = params.get('summary')
    content = params.get('content')
    status = params.get('status')

    if not title or not summary or not content or not status:
        flash("Todos los campos son obligatorios.", "error")
        return redirect(url_for("contents.edit", id=id))

    if status == 'Publicado':
        content_repository.update_content(
            id,
            title=title,
            summary=summary,
            content=content,
            status=status,
            publication_date=datetime.now()
        )
    else:
        content_repository.update_content(
            id,
            title=title,
            summary=summary,
            content=content,
            status=status
        )

    flash("Contenido actualizado con éxito.", "info")
    return redirect(url_for("contents.index"))

# Delete content
@bp.get("/<int:id>/delete")
@has_permission("content_destroy")
def delete(id):
    if content_repository.delete_content(id):
        flash("Contenido eliminado con éxito.", "info")
        return redirect(url_for("contents.index"))
    else:
        flash("Contenido no encontrado.", "error")
        return redirect(url_for("contents.index"))