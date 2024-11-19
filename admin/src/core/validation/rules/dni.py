import re
from ..validator import ValidationRule

class DNIFormat(ValidationRule):
    def validate(self, value: str) -> str | None:
        if not value:
            return None
        pattern = r'^\d{0,3}\.?\d{3}\.?\d{3}[A-Z]$'
        if not re.match(pattern, value):
            return "Formato de DNI inválido"
        return None
