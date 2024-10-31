from src.core.models.role import Role
from src.core.models.user import User
from ..validator import MinLength, ValidationRule, Validator, Required
from src.core.validation.rules.email import EmailFormat

class PasswordStrength(ValidationRule):
    def __init__(self, min_length: int = 8):
        self.min_length = min_length

    def validate(self, value: str) -> str | None:
        if not value:
            return None

        errors = []
        if len(value) < self.min_length:
            errors.append(f"Password must be at least {self.min_length} characters")
        if not any(c.isupper() for c in value):
            errors.append("Password must contain at least one uppercase letter")
        if not any(c.islower() for c in value):
            errors.append("Password must contain at least one lowercase letter")
        if not any(c.isdigit() for c in value):
            errors.append("Password must contain at least one number")

        return " and ".join(errors) if errors else None

class UniqueEmail(ValidationRule):
    def __init__(self, user_model, exclude_id: int = None):
        self.User = user_model
        self.exclude_id = exclude_id

    def validate(self, value: str) -> str | None:
        if not value:
            return None

        query = self.User.query.filter_by(email=value)
        if self.exclude_id:
            query = query.filter(self.User.id != self.exclude_id)

        if query.first():
            return "This email is already registered"
        return None

class ValidRole(ValidationRule):
    def __init__(self, role_model):
        self.Role = role_model

    def validate(self, value: int) -> str | None:
        if not value:
            return None

        role = self.Role.query.get(value)
        if not role:
            return "Invalid role selected"
        return None


class UserValidator(Validator):
    def __init__(self, user_model=User, role_model=Role, user_id: int = None, check_password: bool = True):
        """
        Initialize the user validator.

        Args:
            user_model: The User model class
            role_model: The Role model class
            user_id: The ID of the user being updated (None for new users)
            check_password: Whether to validate password (False for updates where password isn't changed)
        """
        super().__init__()

        # Email validation
        self.add_rule('email', Required())
        self.add_rule('email', EmailFormat())
        self.add_rule('email', UniqueEmail(user_model, exclude_id=user_id))

        # Password validation (only for new users or password changes)
        if check_password:
            self.add_rule('password', Required())
            self.add_rule('password', PasswordStrength(min_length=8))

        # Role validation
        self.add_rule('role_id', Required())
        self.add_rule('role_id', ValidRole(role_model))

        self.add_rule('alias', Required())
        self.add_rule('alias', MinLength(2))

    def validate_for_update(self, data: dict) -> list:
        """
        Special validation for updates that might not include all fields.
        Removes password validation if not provided.
        """
        if 'password' not in data or not data['password']:
            self.rules.pop('password', None)
        return self.validate(data)
