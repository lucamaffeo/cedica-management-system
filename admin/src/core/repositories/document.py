import hashlib
import logging
from typing import BinaryIO, Optional
from minio import Minio
from sqlalchemy import cast, String
from src.core.database import db
from src.core.models.document import Document
from flask import current_app
import uuid

class StorageError(Exception):
    pass

def _get_storage_client() -> Minio:
    """
    Gets the initialized Minio client.

    Returns:
        Minio: The initialized Minio client

    Raises:
        StorageError: If storage is not properly initialized
    """
    if not hasattr(current_app, 'storage'):
        raise StorageError("Storage extension not initialized on Flask app")

    storage_instance = getattr(current_app, 'storage')
    if not storage_instance:
        raise StorageError("Storage instance not found on Flask app")

    client = storage_instance.client
    if not client:
        raise StorageError("Minio client not initialized")

    return client 

def _upload_file(file: BinaryIO, file_path: str) -> str:
    """
    Uploads a file to Minio storage.

    Returns:
        str: The file path in storage
    """
    storage_client = _get_storage_client()
    bucket_name = "grupo10"

    # Ensure bucket exists
    if not storage_client.bucket_exists(bucket_name):
        try:
            storage_client.make_bucket(bucket_name)
            logging.info(f"Created bucket: {bucket_name}")
        except Exception as e:
            raise StorageError(f"Failed to create bucket: {str(e)}")

    # Calculate file length
    file.seek(0, 2)  # Move to the end of the file
    length = file.tell()  # Get the length of the file
    file.seek(0)  # Reset file pointer back to the start

    # Upload file
    try:
        storage_client.put_object(
            bucket_name=bucket_name,
            object_name=file_path,
            data=file,
            length=length,  # Use the actual length of the file
        )
        logging.info(f"Uploaded file to: {file_path}")
        return file_path
    except Exception as e:
        raise StorageError(f"Failed to upload file: {str(e)}")

def list_documents_by_id(type, id, search='', sort_by='title', direction='asc', page=1, items_per_page=5):
    query =Document.query.filter_by(entity_type=type, entity_id=id)

    if search:
        query = query.filter(
            (Document.title.ilike(f'%{search}%')) |
            # Se castea porque document_type es de tipo Enum
            (cast(Document.document_type, String).ilike(f'%{search}%'))
        )

    query = query  # No aplicar filtro, mostrar todos

    # Aplicar ordenación
    if sort_by in ['title', 'upload_date']:
        if direction == 'asc':
            query = query.order_by(getattr(Document, sort_by).asc())
        else:
            query = query.order_by(getattr(Document, sort_by).desc())


    pagination_documents = query.paginate(page=page, per_page=items_per_page, error_out=False)

    return pagination_documents

def create_document(file, entity_type, entity_id,document_type, **kwargs):
    """
    Creates a document and stores it in Minio with a path structure: {module}/{entity_id}/{filename}
    Args:
        file: the file to upload
        entity_type: table of the entity (e.g. employees, riders, horses)
        entity_id: the ID of the entity (e.g. employee_id, rider_id, horse_id)
    """

    

    # Generar un UUID
    unique_id = str(uuid.uuid4())

    # Crear un hash SHA-1 y tomar solo los primeros 8 caracteres
    short_uid = hashlib.sha1(unique_id.encode()).hexdigest()[:8]

    # Generar el nombre del archivo con el hash corto y el nombre original
    file_name = f"{short_uid}-{file.filename}"

    # Construct the Minio path as {module}/{id}/{filename}
    file_path = f"{entity_type}/{entity_id}/{document_type}/{file_name}"
    # upload file
    _upload_file(file, file_path)

    # Add the file path to kwargs to store in the database
    kwargs['file'] = file_path
    kwargs['entity_type'] = entity_type
    kwargs['entity_id'] = entity_id
    kwargs['document_type'] = document_type

    # Create the document in the database
    document = Document(**kwargs)
    db.session.add(document)
    db.session.commit()

    return document

def get_document(id):
    document = Document.query.filter(Document.id == id).first()
    return document

def delete_document(id):
    document = Document.query.filter(Document.id == id).first()
    db.session.delete(document)
    db.session.commit()

    
def update_document(id, **kwargs):
    document = Document.query.filter(Document.id == id).first()
    if not document:
        return None
    for key, value in kwargs.items():
        setattr(document, key, value)
    db.session.commit()
    return document

