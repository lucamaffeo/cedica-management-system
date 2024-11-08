from src.core.validation.validator import Validator, Required, MaxLength, MinLength
from src.core.validation.rules.email import EmailFormat
from src.core.validation.rules.phone import PhoneNumberFormat
from src.core.validation.rules.letters import OnlyLetters
from src.core.validation.rules.unique import Unique  # Importar la nueva regla

class EmployeeValidator(Validator):
    def __init__(self):
        super().__init__()

        self.add_rule('name', Required())
        self.add_rule('name', MaxLength(100))
        self.add_rule('name', OnlyLetters())

        self.add_rule('surname', Required())
        self.add_rule('surname', MaxLength(100))
        self.add_rule('surname', OnlyLetters())

        self.add_rule('dni', Required())
        self.add_rule('dni', MaxLength(20))
        self.add_rule('dni', Unique('employees', 'dni'))  # Agregar regla de unicidad

        self.add_rule('address', MaxLength(255))

        self.add_rule('email', Required())
        self.add_rule('email', EmailFormat())
        self.add_rule('email', MaxLength(120))
        self.add_rule('email', Unique('employees', 'email'))  # Agregar regla de unicidad

        self.add_rule('city', MaxLength(100))
        self.add_rule('city', OnlyLetters())

        self.add_rule('telephone', MaxLength(50))
        self.add_rule('telephone', PhoneNumberFormat())

        self.add_rule('start_date', Required())

        self.add_rule('emergency_contact_info', MaxLength(150))

        self.add_rule('social_work', MaxLength(50))

        self.add_rule('associate_number', MaxLength(50))
        self.add_rule('associate_number', Unique('employees', 'associate_number'))  # Agregar regla de unicidad

        self.add_rule('condition', Required())
        self.add_rule('condition', MaxLength(50))

    def validate_create(self, data):
        return self.validate(data)

    def validate_update(self, data, employee_id):
        self.rules.pop('email', Required)
        self.rules.pop('dni', Required)
        self.rules.pop('associate_number', Required)
        return self.validate(data)
