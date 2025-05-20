from src.core.validation.validator import ValidationError, Validator, Required, MaxLength, In
from src.core.validation.rules.letters import OnlyLetters
from src.core.validation.rules.date import dateFormat
from src.core.repositories import employee as employee_repo


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

    def validate_trainer_ids(self, trainer_ids):
        errors = []
        try:
            trainer_ids = [int(trainer_id) for trainer_id in trainer_ids]
        except ValueError:
            errors.append(ValidationError(field="trainer_id", message="Todos los IDs de entrenadores deben ser enteros."))
            return errors

        for trainer_id in trainer_ids:
            if not employee_repo.get_employee(trainer_id):
                errors.append(ValidationError(field="trainer_id", message=f"ID de entrenador inválido: {trainer_id}"))
        return errors
