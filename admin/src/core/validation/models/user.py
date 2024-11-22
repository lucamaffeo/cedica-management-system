from src.core.models.role import Role
from src.core.models.user import User
from src.core.repositories import user as user_repo, role as role_repo
from ..validator import MinLength, MaxLength, ValidationError, ValidationRule, Validator, Required
from src.core.validation.rules.email import EmailFormat


class PasswordStrength(ValidationRule):
    def __init__(self, min_length: int = 8):
        self.min_length = min_length

    def validate(self, value: str) -> str | None:
        if not value:
            return None

        errors = []
        if len(value) < self.min_length:
            errors.append(
                f"La contraseña debe tener al menos {self.min_length} caracteres")
        if not any(c.isupper() for c in value):
            errors.append(
                "La contraseña debe contener al menos una letra mayúscula")
        if not any(c.islower() for c in value):
            errors.append(
                "La contraseña debe contener al menos una letra minúscula")
        if not any(c.isdigit() for c in value):
            errors.append("La contraseña debe contener al menos un número")

        return ", ".join(errors) if errors else None


class UniqueEmail(ValidationRule):
    def __init__(self, user_model, exclude_id: int = None):
        self.User = user_model
        self.exclude_id = exclude_id

    def validate(self, value: str) -> str | None:
        if not value:
            return None

        user = user_repo.find_user_by_email(value)

        if user and self.exclude_id:
            user = user.filter(self.User.id != self.exclude_id)

        if user:
            return "Este correo electrónico ya está registrado"
        return None


class ValidRole(ValidationRule):
    def __init__(self, role_model):
        self.Role = role_model

    def validate(self, value: int) -> str | None:
        if not value:
            return None

        role = role_repo.get_role_by_id(value)
        if not role:
            return "Rol seleccionado no válido"
        return None


class UserValidator(Validator):
    def __init__(self, user_model=User, role_model=Role, user_id: int = None, check_password: bool = True, is_update_own: bool = False):
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
        self.add_rule('email', MaxLength(255))
        self.add_rule('email', EmailFormat())
        self.add_rule('email', UniqueEmail(user_model, exclude_id=user_id))

        # Password validation (only for new users or password changes)
        if check_password:
            self.add_rule('password', Required())
            self.add_rule('password', MaxLength(64))
            self.add_rule('password', PasswordStrength(min_length=8))

        # Role validation
    # For own profile updates, remove role validation
        if not is_update_own:
            self.add_rule('role_id', Required())
            self.add_rule('role_id', ValidRole(role_model))

        self.add_rule('alias', Required())
        self.add_rule('alias', MaxLength(255))
        self.add_rule('alias', MinLength(2))

    def validate_for_update(self, data: dict) -> list[ValidationError]:
        """
        Validate user data for updates.
        Args:
            data: The user data to validate
        Returns:
            A list of validation errors
        """
        self.rules.pop('email', Required)

        return self.validate(data)
