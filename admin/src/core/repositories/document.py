from src.core.database import db
from src.core.models.document import Document

def list_documents():
    documents = Document.query.all()
    return documents

def create_document(**kwargs):
    document = Document(**kwargs)
    db.session.add(document)
    db.session.commit()

    return document