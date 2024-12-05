from src.core.validation.validator import Validator, Required, MaxLength, In
from src.core.validation.rules.letters import OnlyLetters
from src.core.validation.rules.date import dateFormat


class HorseValidator(Validator):
    def __init__(self):
        super().__init__()

        assigned_activities_ja =['Hipoterapia', 'Monta Terapeutica', 'Deporte Ecuestre Adaptado',
                                    'Actividades Recreativas', 'Equitación']

        self.add_rule('name', Required())
        self.add_rule('name', MaxLength(100))
        self.add_rule('name', OnlyLetters())

        self.add_rule('birth_date', Required())
        self.add_rule('birth_date', dateFormat())

        self.add_rule('gender', Required())
        self.add_rule('gender', MaxLength(50))
        self.add_rule('gender', OnlyLetters())

        self.add_rule('breed', Required())
        self.add_rule('breed', MaxLength(50))
        self.add_rule('breed', OnlyLetters())

        self.add_rule('coat', Required())
        self.add_rule('coat', MaxLength(50))
        self.add_rule('coat', OnlyLetters())

        self.add_rule('purchase_donation', Required())
        self.add_rule('purchase_donation', MaxLength(50))

        self.add_rule('entry_date', Required())
        self.add_rule('entry_date', dateFormat())

        self.add_rule('assigned_location', Required())
        self.add_rule('assigned_location', MaxLength(100))

        self.add_rule('assigned_activities_ja', Required())
        self.add_rule('assigned_activities_ja', MaxLength(50))
        self.add_rule('assigned_activities_ja', In(assigned_activities_ja))

    def validate_create(self, data):
        return self.validate(data)

    def validate_update(self, data, horse_id):
        return self.validate(data)
