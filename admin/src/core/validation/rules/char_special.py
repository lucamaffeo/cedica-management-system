import re
from ..validator import ValidationRule

class OnlyLettersWithSpecialChars(ValidationRule):
    def validate(self, value: str) -> str | None:
        if not value:
            return None
        # Permitir letras, espacios y algunos caracteres especiales como '/'
        pattern = r'^[a-zA-ZáéíóúÁÉÍÓÚñÑ\s\/]+$'
        if not re.match(pattern, value):
            return "contiene caracteres no permitidos"
        return None