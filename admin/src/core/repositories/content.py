from flask import current_app
from src.core.database import db
from src.core.models.content import Content, ContentStatus
from src.core.models.user import User
from sqlalchemy.orm import joinedload
from datetime import datetime
from datetime import timedelta
from flask import jsonify

def create_content(**kwargs):
    content = Content(**kwargs)
    db.session.add(content)
    db.session.commit()

    return content

def total_contents():
    total = Content.query.count()
    return total

def list_contents_api(author=None, published_from=None, published_to=None, page=1, per_page=10):
    # Aplicar filtro por alias del autor
    if author:
        query = Content.query.options(joinedload(Content.author))
        query = query.join(User).filter(User.alias.ilike(f'%{author}%'))
    else:
        query = Content.query

    # Si no manda las dos, no se aplica el filtro !
    if published_from and published_to:
        print(published_from)
        published_from = datetime.fromisoformat(published_from.replace("Z", "+00:00"))
        print(published_from)
        print(published_to)
        published_to = datetime.fromisoformat(published_to.replace("Z", "+00:00"))  # Convert str to date, so we can add timedelta (to make end_date include that day on results)
        print(published_to)
        query = query.filter(Content.publication_date >= published_from, Content.publication_date < published_to + timedelta(days=1))

    articles = query.paginate(page=page, per_page=per_page, error_out=False)
    return articles

def list_contents(search='', status_id=None, sort_by='title', direction='asc', page=1):
    query = Content.query

    if search:
        query = query.filter(
            (Content.title.ilike(f'%{search}%')) |
            (Content.summary.ilike(f'%{search}%')) |
            (Content.content.ilike(f'%{search}%'))
        )
    if status_id:
        query = query.filter(Content.status_id == status_id)
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

def list_statuses():
    return ContentStatus.query.all()

def create_status(name):
    status = ContentStatus(name=name)
    db.session.add(status)
    db.session.commit()
    return status