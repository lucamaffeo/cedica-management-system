from flask import Blueprint, redirect, render_template, request, url_for, flash
from src.core.validation.models.contact import ContactValidator
from src.core.repositories import contact as contact_repo
from src.web.helpers.flash import flash_validation_errors
from src.web.helpers.auth import has_permission

bp = Blueprint("contacts", __name__, url_prefix="/contacts")

@bp.post("/create")
@has_permission("contact_create")
def store():
    data = request.form.to_dict()
    validator = ContactValidator()

    errors = validator.validate_for_create(data)
    if errors:
        flash_validation_errors(errors)
        return redirect(url_for("contacts.create"))

    contact_repo.create_contact(
        title=data["title"],
        email=data["email"],
        description=data["description"],
    )

    flash("Contacto creado con éxito.", "success")
    return redirect(url_for("contacts.index"))

@bp.get("/<int:id>/update")
@has_permission("contact_update")
def edit(id):
    contact = contact_repo.get_contact(id)
    if not contact:
        flash("Contacto no encontrado.", "error")
        return redirect(url_for("contacts.index"))
    return render_template("contacts/form.html", is_update=True, title='Actualizar Contacto', contact=contact, statuses=contact_repo.list_statuses())

@bp.route("/<int:id>/update", methods=["POST", "PATCH"])
@has_permission("contact_update")
def update(id):
    data = request.form.to_dict()
    # remove status if empty
    if data.get('status') == '':
        data.pop('status')

    validator = ContactValidator(contact_id=id)

    errors = validator.validate_for_update(data)
    if errors:
        flash_validation_errors(errors)
        return redirect(url_for("contacts.edit", id=id))

    if contact_repo.update_contact(
        id=id,
        status_id=data.get("status", None),
        comment=data.get("comment"),
        updated_by=data.get("updated_by"),
    ):
        flash("Contacto actualizado con éxito.", "success")
        return redirect(url_for("contacts.index"))
    else:
        flash("Contacto no encontrado o estado invalido.", "error")
        return redirect(url_for("contacts.index"))

@bp.get("/<int:id>/show")
@has_permission("contact_show")
def show(id):
    contact = contact_repo.get_contact(id)
    if not contact:
        flash("Contacto no encontrado.", "error")
        return redirect(url_for("contacts.index"))
    return render_template("contacts/show.html", contact=contact)

@bp.get("/<int:id>/delete")
@has_permission("contact_destroy")
def delete(id):
    if contact_repo.delete_contact(id):
        flash("Contacto eliminado con éxito.", "info")
        return redirect(url_for("contacts.index"))
    else:
        flash("Contacto no encontrado.", "error")
        return redirect(url_for("contacts.index"))

@bp.get("/")
@has_permission("contact_index")
def index():
    sort_by = request.args.get('sort_by', 'title')
    direction = request.args.get('direction', 'asc')
    page = request.args.get('page', 1, type=int)
    status_id = request.args.get('status', None, type=int)

    contacts = contact_repo.list_contacts(sort_by, direction, status_id, page)

    if not contacts.items:
        flash("No se encontraron contactos.", "info")
    return render_template("contacts/index.html", pagination=contacts, statuses=contact_repo.list_statuses())
