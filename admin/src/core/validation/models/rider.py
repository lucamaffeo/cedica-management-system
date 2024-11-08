from src.core.validation.validator import Validator, Required, MaxLength, MinLength
from src.core.validation.rules.email import EmailFormat
from src.core.validation.rules.phone import PhoneNumberFormat
from src.core.validation.rules.letters import OnlyLetters
from src.core.validation.rules.numbers import OnlyNumbers
from src.core.validation.rules.unique import Unique

class RiderValidator(Validator):
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
        self.add_rule('dni', Unique())

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
        self.add_rule('emergency_contact', PhoneNumberFormat())
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


        
        self.add_rule('institution_phone','phone', Required())
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
        self.add_rule('tutor_address', MaxLength(255))
        self.add_rule('tutor_cellphone', PhoneNumberFormat())
        self.add_rule('tutor_cellphone', MaxLength(50))
        self.add_rule('tutor_email', EmailFormat())
        self.add_rule('tutor_email', MaxLength(100))
        self.add_rule('tutor_educational_level', MaxLength(50))
        self.add_rule('tutor_occupation', MaxLength(100))

    def validate_create(self, data):
        return self.validate(data)

    def validate_update(self, data, rider_id):
        self.rules.pop('dni', Required)
        return self.validate(data)