from flask import current_app
from src.core.database import db
from src.core.models.content import Content, ContentStatus
from src.core.models.user import User
from sqlalchemy.orm import joinedload
from datetime import datetime
from datetime import timedelta
from flask import jsonify


def create_content(**kwargs):
    """
    Crea un nuevo contenido y lo agrega a la base de datos.

    Args:
        **kwargs: Argumentos de palabra clave para los atributos del contenido.

    Returns:
        Content: El objeto contenido creado.
    """
    content = Content(**kwargs)
    db.session.add(content)
    db.session.commit()

    return content


def list_contents_api(author=None, published_from=None, published_to=None, page=1, per_page=10):
    """
    Lista contenidos para la API con filtros opcionales y paginación.

    Args:
        author (str): Alias del autor para filtrar contenidos.
        published_from (str): Fecha de inicio para filtrar contenidos.
        published_to (str): Fecha de fin para filtrar contenidos.
        page (int): Número de página para la paginación.
        per_page (int): Número de elementos por página.

    Returns:
        Pagination: Lista paginada de contenidos.
    """
    # Aplicar filtro por alias del autor
    query = Content.query.join(ContentStatus).filter(
        ContentStatus.name == "Publicado")

    if author:
        query = query.options(joinedload(Content.author))
        query = query.join(User).filter(User.alias.ilike(f'%{author}%'))

    if published_from:
        published_from = datetime.fromisoformat(published_from.replace("Z", "+00:00"))
        query = query.filter(Content.publication_date >= published_from)

    if published_to:
        published_to = datetime.fromisoformat(published_to.replace("Z", "+00:00"))
        # Add one day to include the entire end date
        query = query.filter(Content.publication_date < published_to + timedelta(days=1))


    query = query.order_by(Content.publication_date.desc())

    articles = query.paginate(page=page, per_page=per_page, error_out=False)
    return articles


def list_contents(search='', status_id=None, sort_by='title', direction='asc', page=1):
    """
    Lista contenidos con búsqueda, filtro y ordenación opcionales.

    Args:
        search (str): Término de búsqueda para los atributos del contenido.
        status_id (int): ID del estado para filtrar contenidos.
        sort_by (str): Atributo por el cual ordenar.
        direction (str): Dirección de ordenación ('asc' o 'desc').
        page (int): Número de página para la paginación.

    Returns:
        Pagination: Lista paginada de contenidos.
    """
    query = Content.query

    if search:
        query = query.filter(
            (Content.title.ilike(f'%{search}%')) |
            (Content.summary.ilike(f'%{search}%')) 
        )
    if status_id:
        query = query.filter(Content.status_id == status_id)
    else:
        query = query  # No aplicar filtro, mostrar todos

    items_per_page = current_app.config.get('ITEMS_PER_PAGE')

    # Aplicar ordenación
    if sort_by in ['title', 'update_date']:
        if direction == 'asc':
            query = query.order_by(getattr(Content, sort_by).asc())
        else:
            query = query.order_by(getattr(Content, sort_by).desc())

    pagination_contents = query.paginate(
        page=page, per_page=items_per_page, error_out=False)

    return pagination_contents


def get_content(id):
    """
    Recupera un contenido por ID.

    Args:
        id (int): El ID del contenido.

    Returns:
        Content: El objeto contenido o None si no se encuentra.
    """
    content = Content.query.filter(Content.id == id).first()
    return content


def update_content(id, **kwargs):
    """
    Actualiza los atributos de un contenido.

    Args:
        id (int): El ID del contenido.
        **kwargs: Argumentos de palabra clave para los atributos del contenido.

    Returns:
        bool: True si la actualización fue exitosa, False en caso contrario.
    """
    content = Content.query.filter(Content.id == id).first()
    if not content:
        return False
    for key, value in kwargs.items():
        setattr(content, key, value)
    db.session.commit()
    return True


def delete_content(id):
    """
    Elimina un contenido por ID.

    Args:
        id (int): El ID del contenido.

    Returns:
        bool: True si la eliminación fue exitosa, False en caso contrario.
    """
    content = Content.query.filter(Content.id == id).first()
    if content:
        db.session.delete(content)
        db.session.commit()
        return True
    return False


def list_statuses():
    """
    Lista todos los estados de contenido.

    Returns:
        list: Lista de todos los estados de contenido.
    """
    return ContentStatus.query.all()


def create_status(name):
    """
    Crea un nuevo estado de contenido y lo agrega a la base de datos.

    Args:
        name (str): El nombre del estado.

    Returns:
        ContentStatus: El objeto estado de contenido creado.
    """
    status = ContentStatus(name=name)
    db.session.add(status)
    db.session.commit()
    return status
