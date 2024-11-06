import re
from flask import Blueprint, redirect, render_template, request, url_for, flash
from src.core.repositories import content as content_repository
from src.web.helpers.auth import has_permission
from flask import current_app


bp = Blueprint("contents", __name__, url_prefix="/contents")

bp.get("/")
@has_permission("content_index")
def index():
    search = request.args.get('search')
    status = request.args.get('status')
    sort_by = request.args.get('sort_by', 'title')
    direction = request.args.get('direction', 'asc')
    page = request.args.get('page', 1, type=int)

    contents = content_repository.list_contents(search, status, sort_by, direction, page)
    return render_template("contents/index.html", pagination=contents)

bp.get("/create")
@has_permission("content_create")
def register():
    return render_template("contents/form.html", is_update=False, title="Crear Contenido")

bp.post("/create")
@has_permission("content_create")
def create():
    params = request.form
    title = params.get('title')
    summary = params.get('summary')
    content = params.get('content')
    author_id = params.get('author_id')
    status = params.get('status')

    if not title or not summary or not content or not author_id or not status:
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

bp.get("/<int:id>/show")
@has_permission("content_show")
def show(id):
    content = content_repository.get_content(id)
    if not content:
        flash("Contenido no encontrado.", "error")
        return redirect(url_for("contents.index"))
    return render_template("contents/show.html", content=content)

bp.get("/<int:id>/edit")
@has_permission("content_edit")
def edit(id):
    content = content_repository.get_content(id)
    if not content:
        flash("Contenido no encontrado.", "error")
        return redirect(url_for("contents.index"))
    return render_template("contents/form.html", is_update=True, title="Editar Contenido", content=content)

bp.post("/<int:id>/edit")
@has_permission("content_edit")
def update(id):
    params = request.form
    title = params.get('title')
    summary = params.get('summary')
    content = params.get('content')
    author_id = params.get('author_id')
    status = params.get('status')

    if not title or not summary or not content or not author_id or not status:
        flash("Todos los campos son obligatorios.", "error")
        return redirect(url_for("contents.edit", id=id))

    content_repository.update_content(
        id,
        title=title,
        summary=summary,
        content=content,
        author_id=author_id,
        status=status
    )

    flash("Contenido actualizado con éxito.", "info")
    return redirect(url_for("contents.index"))
