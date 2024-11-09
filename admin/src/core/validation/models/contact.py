from src.core.models.contact import Contact
from src.core.repositories import contact as contact_repo
from ..validator import MinLength, MaxLength, ValidationError, ValidationRule, Validator, Required
from src.core.validation.rules.email import EmailFormat

class ContactValidator(Validator):
    def __init__(self, contact_id: int = None):
        """
        Initialize the contact validator.

        Args:
            contact_id: The ID of the contact being updated (None for new contacts)
        """
        super().__init__()


    def validate_for_create(self, data: dict) -> list[ValidationError]:
        """
        Validate contact data for creation.
        Args:
            data: The contact data to validate
        Returns:
            A list of validation errors
        """
        self.add_rule('name', Required())
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
        self.add_rule('status', Required())
        self.add_rule('status', Required())

        return self.validate(data)
