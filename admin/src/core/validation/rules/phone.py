
import re
from ..validator import ValidationRule

class PhoneNumberFormat(ValidationRule):
    def validate(self, value: str) -> str | None:
        if not value:
            return None
        pattern = r'^\+?[0-9 ]+$'
        if not re.match(pattern, value):
            return "Formato de número de teléfono inválido"
        return None