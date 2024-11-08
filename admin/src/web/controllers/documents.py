from flask import Blueprint, redirect, render_template, request, url_for, flash, send_file
from src.web.helpers.documentation import clean_entity_type
from src.core.repositories import document as document_repository
from src.web.helpers.auth import has_permission
from src.core.database import db

bp = Blueprint("documents", __name__, url_prefix="/documents")

#list documents
@bp.get("/<string:entity_type>/<int:entity_id>/")
@clean_entity_type
def index(entity_type, entity_id):
    search = request.args.get("search", "")
    sort_by = request.args.get("sort_by", "title")
    direction = request.args.get("direction", "asc")
    page = int(request.args.get("page", 1))

    # Listar documentos por ID del jinete
    documents = document_repository.list_documents_by_id(entity_type, entity_id, search, sort_by, direction, page)

    if not documents.items:
        flash("No se encontraron Documentos.", "info")
    return render_template("documents/index.html", pagination=documents, entity_type=entity_type, entity_id=entity_id)

# destroy document
@bp.get("/<string:entity_type>/<int:entity_id>/<int:id>/delete")
@clean_entity_type
def delete(entity_type, entity_id, id):
    document = document_repository.get_document(id)
    if not document:
        flash("Documento no encontrado.", "error")
        # redirect to last page
        return redirect(request.referrer)

    document_repository.delete_document(id)
    flash("Documento eliminado con éxito.", "info")
    return redirect(url_for("documents.index", entity_type=document.entity_type, entity_id=document.entity_id))

# download document
@bp.get("/<string:entity_type>/<int:entity_id>/<int:id>/dl")
def download(entity_type, entity_id, id):
    document = document_repository.get_document(id)
    if not document:
        flash("Documento no encontrado.", "error")
        return redirect(request.referrer)
    else:
        file_stream, file_name = document_repository.download_file(document.file)
        return send_file(file_stream, as_attachment=True, download_name=file_name)

# add document
@bp.get("/<string:entity_type>/<int:entity_id>/create")
@clean_entity_type
def add(entity_type, entity_id):
    return render_template("documents/form.html", entity_type=entity_type, entity_id=entity_id,title="Agregar documento")

# Create document
@bp.post("/<string:entity_type>/<int:entity_id>/create")
@clean_entity_type
def create(entity_type, entity_id):
    print(f"type: {entity_type}, id: {entity_id}")  # Add this line to check what values are passed
    params = request.form

    required_fields = ['title', 'document_type']
    for field in required_fields:
        if field not in params:
            flash(f"El campo {field} es requerido.", "error")
            return redirect(url_for("documents.add", entity_type=entity_type, entity_id=entity_id))

    # Validar que solo uno de los campos (archivo o enlace) esté presente
    file = request.files.get('file')
    link = params.get('link')

    if bool(file) == (bool(link) or (link and not link.strip())):  # Ambos presentes, ambos ausentes o enlace vacío
        flash("Debe proporcionar un archivo o un enlace, pero no ambos.", "error")
        return redirect(url_for("documents.add", entity_type=entity_type, entity_id=entity_id))

    # Crear el documento
    try:
        document = document_repository.create_document(
            title=params['title'],
            document_type=params['document_type'],
            file=file,
            entity_type=entity_type,
            entity_id=entity_id
        )
        db.session.commit()
        flash("Documento agregado con éxito.", "success")
        return redirect(url_for("documents.index", entity_type=document.entity_type, entity_id=document.entity_id))
    except Exception as e:
        db.session.rollback()
        flash(f"Error al agregar el documento: {str(e)}", "error")
        return redirect(url_for("documents.add", entity_type=entity_type, entity_id=entity_id))
