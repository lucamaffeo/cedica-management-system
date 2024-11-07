from flask import current_app
from src.core.database import db
from src.core.models.contact import Contact, ContactStatus

def list_contacts(sort_by='email', direction='asc', status_id=None, page=1):
    query = Contact.query

    if status_id:
        query = query.filter(Contact.status_id == status_id)

    items_per_page = current_app.config.get('ITEMS_PER_PAGE')

    if direction == 'asc':
        query = query.order_by(getattr(Contact, sort_by).asc())
    else:
        query = query.order_by(getattr(Contact, sort_by).desc())

    paginated_contacts = query.paginate(page=page, per_page=items_per_page, error_out=False)

    return paginated_contacts

def list_statuses():
    contact_status = ContactStatus.query.all()
    return contact_status

def create_contact(**kwargs):
    contact = Contact(**kwargs)
    db.session.add(contact)
    db.session.commit()

    return contact

def create_status(**kwargs):
    status = ContactStatus(**kwargs)
    db.session.add(status)
    db.session.commit()
    return status

def update_contact(id, **kwargs):
    contact = Contact.query.filter(Contact.id == id).first()
    if not contact:
        return False
    for key, value in kwargs.items():
        setattr(contact, key, value)
    db.session.commit()
    return True

def delete_contact(id):
    contact = Contact.query.filter(Contact.id == id).first()
    if contact:
        db.session.delete(contact)
        db.session.commit()
        return True
    return False

def get_contact(id) -> Contact | None:
    contact = Contact.query.filter(Contact.id == id).first()
    return contact
