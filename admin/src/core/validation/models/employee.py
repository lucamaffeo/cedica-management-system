from src.core.models.employee import Employee
from src.core.repositories import employee as employee_repository
from src.core.validation.validator import ValidationRule, Validator, Required, MaxLength, MinLength
from src.core.validation.rules.email import EmailFormat
from src.core.validation.rules.phone import PhoneNumberFormat
from src.core.validation.rules.letters import OnlyLetters

class UniqueDni(ValidationRule):
    def __init__(self, exclude_id = None):
        self.Employee = Employee
        self.exclude_id = exclude_id

    def validate(self, value: str) -> str | None:
        if not value:
            return None

        empl = employee_repository.find_employee_by_dni(value)

        if empl and self.exclude_id:
            empl = empl.filter(self.Employee.id != self.exclude_id)

        if empl:
            return "Este DNI ya está registrado"
        return None

class UniqueEmail(ValidationRule):
    def __init__(self, exclude_id = None):
        self.Employee = Employee
        self.exclude_id = exclude_id
    def validate(self, value: str) -> str | None:
        if not value:
            return None
        empl = employee_repository.get_by_email(value)
        if empl and self.exclude_id:
            empl = empl.filter(self.Employee.id != self.exclude_id)
        if empl:
            return "Este correo electrónico ya está registrado"
        return None

class UniqueAssocNum(ValidationRule):
    def __init__(self, exclude_id = None):
        self.Employee = Employee
        self.exclude_id = exclude_id
    def validate(self, value: str) -> str | None:
        if not value:
            return None
        empl = employee_repository.find_employee_by_associate_number(value)
        if empl and self.exclude_id:
            empl = empl.filter(self.Employee.id != self.exclude_id)
        if empl:
            return "Este número de asociado ya está registrado"
        return None

class EmployeeValidator(Validator):
    def __init__(self, empl_id=None):
        super().__init__()

        self.add_rule('name', Required())
        self.add_rule('name', MaxLength(100))
        self.add_rule('name', OnlyLetters())

        self.add_rule('surname', Required())
        self.add_rule('surname', MaxLength(100))
        self.add_rule('surname', OnlyLetters())

        self.add_rule('dni', Required())
        self.add_rule('dni', MaxLength(20))
        self.add_rule('dni', UniqueDni(empl_id))  # Agregar regla de unicidad

        self.add_rule('address', MaxLength(255))

        self.add_rule('email', Required())
        self.add_rule('email', EmailFormat())
        self.add_rule('email', MaxLength(120))
        self.add_rule('email', UniqueEmail(empl_id))  # Agregar regla de unicidad

        self.add_rule('city', MaxLength(100))
        self.add_rule('city', OnlyLetters())

        self.add_rule('telephone', MaxLength(50))
        self.add_rule('telephone', PhoneNumberFormat())

        self.add_rule('start_date', Required())

        self.add_rule('emergency_contact_info', MaxLength(150))

        self.add_rule('social_work', MaxLength(50))

        self.add_rule('associate_number', MaxLength(50))
        self.add_rule('associate_number', UniqueAssocNum(empl_id))  # Agregar regla de unicidad

        self.add_rule('condition', Required())
        self.add_rule('condition', MaxLength(50))

    def validate_create(self, data):
        return self.validate(data)

    def validate_update(self, data):
        self.rules.pop('email', Required)
        self.rules.pop('dni', Required)
        self.rules.pop('associate_number', Required)
        return self.validate(data)
