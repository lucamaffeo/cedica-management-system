from sqlalchemy import cast, String
from src.core.database import db
from src.core.models.document import Document

def list_documents_by_id(id, search='', sort_by='title', direction='asc', page=1, items_per_page=5):
    query =Document.query.filter_by(rider_id=id)

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

def create_document(**kwargs):
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
