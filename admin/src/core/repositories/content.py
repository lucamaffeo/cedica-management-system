from flask import current_app
from src.core.database import db
from src.core.models.content import Content

def create_content(**kwargs):
    content = Content(**kwargs)
    db.session.add(content)
    db.session.commit()

    return content

def list_contents(search='', status=None, sort_by='title', direction='asc', page=1):
    query = Content.query

    if search:
        query = query.filter(
            (Content.title.ilike(f'%{search}%')) |
            (Content.summary.ilike(f'%{search}%')) |
            (Content.content.ilike(f'%{search}%'))
        )
    if status:
        query = query.filter(Content.status == status)
    else:
        query = query  # No aplicar filtro, mostrar todos

    items_per_page = current_app.config.get('ITEMS_PER_PAGE')

    # Aplicar ordenación
    if sort_by in ['title', 'publication_date', 'creation_date']:
        if direction == 'asc':
            query = query.order_by(getattr(Content, sort_by).asc())
        else:
            query = query.order_by(getattr(Content, sort_by).desc())

    pagination_contents = query.paginate(page=page, per_page=items_per_page, error_out=False)

    return pagination_contents

def get_content(id):
    content = Content.query.filter(Content.id == id).first()
    return content

def update_content(id, **kwargs):
    content = Content.query.filter(Content.id == id).first()
    if not content:
        return False
    for key, value in kwargs.items():
        setattr(content, key, value)
    db.session.commit()
    return True

def delete_content(id):
    content = Content.query.filter(Content.id == id).first()
    if content:
        db.session.delete(content)
        db.session.commit()
        return True
    return False