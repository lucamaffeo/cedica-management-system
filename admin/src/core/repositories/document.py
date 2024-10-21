from src.core.database import db
from src.core.models.document import Document


def list_documents_by_id(id, search='', sort_by='name', direction='asc', page=1, items_per_page=5):
    query = Document.query

    if search:
        query = query.filter(
            (Document.title.ilike(f'%{search}%')) |
            (Document.document_type.ilike(f'%{search}%')) 
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