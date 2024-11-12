from src.core.validation.validator import MinLength, MaxLength, ValidationError, ValidationRule, Validator, Required
from src.core.repositories import content as content_repo
class StatusTransitionRule(ValidationRule):
    def __init__(self, content_id: int):
        self.content_id = content_id

    def validate(self, value) -> list[ValidationError]:
        errors = []
        try:
            new_status = int(value)
            # Obtener el contenido actual para verificar su estado
            current_content = content_repo.get_content(self.content_id)

            if current_content is None:
                errors.append('Contenido inválido')
                return errors

            current_status = current_content.status_id

            # Verificar si el estado está dentro del rango válido
            if new_status > 3:
                errors.append('El estado no puede ser mayor que 3')
                return errors

            # Verificar si el incremento del estado es exactamente 1
            if new_status != current_status + 1:
                errors.append('El estado solo puede incrementarse en 1')
        except (ValueError, TypeError):
            errors.append('El estado debe ser un número válido')

        return errors

class ContentValidator(Validator):
    def __init__(self, content_id: int = None):
        super().__init__()
        self.content_id = content_id

    def validate_for_create(self, data: dict) -> list[ValidationError]:
        self.add_rule('title', Required())
        self.add_rule('title', MaxLength(255))
        self.add_rule('title', MinLength(2))

        self.add_rule('summary', Required())
        self.add_rule('summary', MaxLength(255))
        self.add_rule('summary', MinLength(2))

        self.add_rule('content', Required())
        self.add_rule('content', MinLength(10))

        return self.validate(data)

    def validate_for_update(self, data: dict) -> list[ValidationError]:
        if self.content_id and 'status' in data and data['status']:
            self.add_rule('status', StatusTransitionRule(self.content_id))
        return self.validate_for_create(data)