from src.core.models.contact import Contact
from src.core.repositories import contact as contact_repo
from ..validator import MinLength, MaxLength, ValidationError, ValidationRule, Validator, Required
from src.core.validation.rules.email import EmailFormat

class StatusTransitionRule(ValidationRule):
    def __init__(self, contact_id: int):
        self.contact_id = contact_id

    def validate(self, value) -> list[ValidationError]:
        errors = []
        try:
            new_status = int(value)
            # Get current contact to check its status
            current_contact = contact_repo.get_contact(self.contact_id)

            if current_contact is None:
                errors.append('Contacto inválido')
                return errors

            current_status = current_contact.status_id

            # Check if status is within valid range
            if new_status > 3:
                errors.append('El estado no puede ser mayor que 3')
                return errors

            # Check if status increment is exactly 1
            if new_status != current_status + 1:
                errors.append('El estado solo puede incrementarse en 1')
        except (ValueError, TypeError):
            errors.append('El estado debe ser un número válido')

        return errors


class ContactValidator(Validator):
    def __init__(self, contact_id: int = None):
        """
        Initialize the contact validator.

        Args:
            contact_id: The ID of the contact being updated (None for new contacts)
        """
        super().__init__()
        self.contact_id = contact_id


    def validate_for_create(self, data: dict) -> list[ValidationError]:
        """
        Validate contact data for creation.
        Args:
            data: The contact data to validate
        Returns:
            A list of validation errors
        """
        self.add_rule('name', MaxLength(255))
        self.add_rule('name', MinLength(2))

        self.add_rule('title', Required())
        self.add_rule('title', MaxLength(255))
        self.add_rule('title', MinLength(2))

        self.add_rule('email', Required())
        self.add_rule('email', MaxLength(255))
        self.add_rule('email', EmailFormat())

        self.add_rule('description', MaxLength(20))
        self.add_rule('description', Required())
        return self.validate(data)

    def validate_for_update(self, data: dict) -> list[ValidationError]:
        """
        Validate contact data for updates.
        Args:
            data: The contact data to validate
        Returns:
            A list of validation errors
        """
        if self.contact_id and 'status' in data:
            self.add_rule('status', StatusTransitionRule(self.contact_id))

        return self.validate(data)
