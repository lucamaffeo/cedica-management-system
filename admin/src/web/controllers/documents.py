import io
from flask import Blueprint, redirect, render_template, request, url_for, flash, send_file
from src.core.validation.models.document import DocumentValidator
from src.web.helpers.flash import flash_validation_errors
from src.web.helpers.documentation import clean_entity_type
from src.core.repositories import document as document_repository
from src.web.helpers.auth import has_permission

bp = Blueprint("documents", __name__, url_prefix="/documents")

# list documents


@bp.get("/<string:entity_type>/<int:entity_id>/")
@clean_entity_type
def index(entity_type, entity_id):
    """
    Renderiza la página de índice de documentos con paginación y filtros.
    
    :param entity_type: Tipo de entidad a la que pertenece el documento.
    :param entity_id: ID de la entidad a la que pertenece el documento.
    """
    search = request.args.get("search", "")
    sort_by = request.args.get("sort_by", "title")
    direction = request.args.get("direction", "asc")
    page = request.args.get('page', 1, type=int)

    # Listar documentos por ID del jinete
    documents = document_repository.list_documents_by_id(
        entity_type, entity_id, search, sort_by, direction, page)

    if not documents.items:
        flash("No se encontraron Documentos.", "info")
    return render_template("documents/index.html", pagination=documents, entity_type=entity_type, entity_id=entity_id)

# destroy document


@bp.get("/<string:entity_type>/<int:entity_id>/<int:id>/delete")
@clean_entity_type
def delete(entity_type, entity_id, id):
    """
    Elimina un documento específico.
    
    :param entity_type: Tipo de entidad a la que pertenece el documento.
    :param entity_id: ID de la entidad a la que pertenece el documento.
    :param id: ID del documento a eliminar.
    """
    if document_repository.delete_document(id):
        flash("Documento eliminado con éxito.", "info")
        return redirect(url_for("documents.index", entity_type=entity_type, entity_id=entity_id))
    else:
        flash("Documento no encontrado.", "error")
        return redirect(request.referrer)

# download document


@bp.get("/<string:entity_type>/<int:entity_id>/<int:id>/dl")
def download(entity_type, entity_id, id):
    """
    Descarga un documento específico.
    
    :param entity_type: Tipo de entidad a la que pertenece el documento.
    :param entity_id: ID de la entidad a la que pertenece el documento.
    :param id: ID del documento a descargar.
    """
    document = document_repository.get_document(id)
    if not document:
        flash("Documento no encontrado.", "error")
        return redirect(request.referrer)
    else:
        file_data, file_name = document_repository.download_file(document.file)
        return send_file(
            io.BytesIO(file_data),
            as_attachment=True,
            download_name=file_name
        )

# add document


@bp.get("/<string:entity_type>/<int:entity_id>/create")
@clean_entity_type
def add(entity_type, entity_id):
    """
    Renderiza el formulario para agregar un nuevo documento.
    
    :param entity_type: Tipo de entidad a la que pertenece el documento.
    :param entity_id: ID de la entidad a la que pertenece el documento.
    """
    return render_template("documents/form.html", entity_type=entity_type, entity_id=entity_id, title="Agregar documento")

# Create document


@bp.post("/<string:entity_type>/<int:entity_id>/create")
@clean_entity_type
def create(entity_type, entity_id):
    """
    Crea un nuevo documento basado en los datos del formulario.
    
    :param entity_type: Tipo de entidad a la que pertenece el documento.
    :param entity_id: ID de la entidad a la que pertenece el documento.
    """
    params = request.form.to_dict()
    # agregar entity_type y entity_id a los parámetros
    params['entity_type'] = entity_type
    params['entity_id'] = entity_id

    # Validar que solo uno de los campos (archivo o enlace) esté presente
    if params.get('doc_enl') == 'file':
        file = request.files.get('file')

        if not file or file.filename.strip() == '':
            flash("Debe cargar un archivo si selecciona 'Documento'.", "error")
            return redirect(url_for("documents.add", entity_type=entity_type, entity_id=entity_id))
        else:
            params['link'] = ''
            link = None
            params['filename'] = file.filename
    else:
        link = params.get('link')
        file = None
        if not link or link.strip() == '':
            flash("Debe proporcionar un enlace si selecciona 'Enlace'.", "error")
            return redirect(url_for("documents.add", entity_type=entity_type, entity_id=entity_id))

    # Llamada al validator
    validator = DocumentValidator()
    errors = validator.validate_create(params)
    if errors:
        flash_validation_errors(errors)
        return redirect(url_for("documents.add", entity_type=entity_type, entity_id=entity_id))

    # Crear el documento
    try:
        document = document_repository.create_document(
            title=params['title'],
            document_type=params['document_type'],
            file=file if file else link,
            entity_type=entity_type,
            entity_id=entity_id
        )
        flash("Documento agregado con éxito.", "success")
        return redirect(url_for("documents.index", entity_type=document.entity_type, entity_id=document.entity_id))
    except Exception as e:
        flash(f"Error al agregar el documento: {str(e)}", "error")
        return redirect(url_for("documents.add", entity_type=entity_type, entity_id=entity_id))
