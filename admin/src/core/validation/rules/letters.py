import re
from ..validator import ValidationRule


class OnlyLetters(ValidationRule):
    def validate(self, value: str) -> str | None:
        if not value:
            return None
        pattern = r'^[a-zA-Z]+$'
        if not re.match(pattern, value):
            return "Solo puede contener letras"
        return None
