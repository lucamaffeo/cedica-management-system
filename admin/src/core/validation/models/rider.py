from src.core.validation.rules.dni import DNIFormat
from src.core.models.rider import Rider
from src.core.validation.validator import ValidationRule, Validator, Required, MaxLength, MinLength
from src.core.validation.rules.email import EmailFormat
from src.core.validation.rules.phone import PhoneNumberFormat
from src.core.validation.rules.letters import OnlyLetters
from src.core.validation.rules.numbers import OnlyNumbers
from src.core.repositories import riders as rider_repository

class UniqueDni(ValidationRule):
    def __init__(self, exclude_id = None):
        self.Rider = Rider
        self.exclude_id = exclude_id

    def validate(self, value: str) -> str | None:
        if not value:
            return None

        user = rider_repository.find_rider_by_dni(value)

        if user and self.exclude_id:
            user = user.filter(self.Rider.id != self.exclude_id)

        if user:
            return "Este DNI ya está registrado"
        return None

class RiderValidator(Validator):
    def __init__(self, rider_id = None):
        super().__init__()

        self.add_rule('name', Required())
        self.add_rule('name', MaxLength(100))
        self.add_rule('name', OnlyLetters())

        self.add_rule('surname', Required())
        self.add_rule('surname', MaxLength(100))
        self.add_rule('surname', OnlyLetters())

        self.add_rule('dni', Required())
        self.add_rule('dni', MaxLength(20))
        self.add_rule('dni', DNIFormat())
        self.add_rule('dni', UniqueDni(rider_id))

        self.add_rule('age', Required())
        self.add_rule('age', MaxLength(3))
        self.add_rule('age', OnlyNumbers())

        self.add_rule('birthdate', Required())

        self.add_rule('birth_place', Required())
        self.add_rule('birth_place', MaxLength(100))

        self.add_rule('address', Required())
        self.add_rule('address', MaxLength(255))

        self.add_rule('phone', Required())
        self.add_rule('phone', PhoneNumberFormat())
        self.add_rule('phone', MaxLength(50))

        self.add_rule('emergency_contact', Required())
        self.add_rule('emergency_contact', OnlyLetters())
        self.add_rule('emergency_contact', MaxLength(100))

        self.add_rule('emergency_contact_phone_number', Required())
        self.add_rule('emergency_contact_phone_number', PhoneNumberFormat())
        self.add_rule('emergency_contact_phone_number', MaxLength(50))

        self.add_rule('professionals', Required())
        self.add_rule('professionals', MaxLength(255))


        self.add_rule('health_insurance', Required())
        self.add_rule('health_insurance', MaxLength(100))

        self.add_rule('affiliate_number', Required())
        self.add_rule('affiliate_number', MaxLength(50))

        self.add_rule('observations', MaxLength(255))

        self.add_rule('school_institution', Required())
        self.add_rule('school_institution', MaxLength(100))

        self.add_rule('institution_address', Required())
        self.add_rule('institution_address', MaxLength(255))

        self.add_rule('grade', Required())
        self.add_rule('grade', MaxLength(50))


        self.add_rule('institution_phone', Required())
        self.add_rule('institution_phone', PhoneNumberFormat())
        self.add_rule('institution_phone', MaxLength(50))

        self.add_rule('institution_observations', MaxLength(255))

        self.add_rule('work_proposal', Required())
        self.add_rule('work_proposal', MaxLength(255))

        self.add_rule('condition', Required())
        self.add_rule('condition', MaxLength(50))

        self.add_rule('headquarters', Required())
        self.add_rule('headquarters', MaxLength(100))


        #aqui lo que no son requeridos
        self.add_rule('tutor_relationship', MaxLength(50))
        self.add_rule('tutor_name', MaxLength(100))
        self.add_rule('tutor_surname', MaxLength(100))
        self.add_rule('tutor_dni', MaxLength(20))
        self.add_rule('tutor_dni', DNIFormat())
        self.add_rule('tutor_address', MaxLength(255))
        self.add_rule('tutor_cellphone', PhoneNumberFormat())
        self.add_rule('tutor_cellphone', MaxLength(50))
        self.add_rule('tutor_email', EmailFormat())
        self.add_rule('tutor_email', MaxLength(100))
        self.add_rule('tutor_educational_level', MaxLength(50))
        self.add_rule('tutor_occupation', MaxLength(100))

    def validate_create(self, data):
        return self.validate(data)

    def validate_update(self, data):
        self.rules.pop('dni', Required)
        return self.validate(data)
