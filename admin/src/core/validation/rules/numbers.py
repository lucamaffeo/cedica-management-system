import re
from ..validator import ValidationRule

class OnlyNumbers(ValidationRule):
    def validate(self, value: str) -> str | None:
        if not value:
            return None
        pattern = r'^[0-9]+$'
        if not re.match(pattern, value):
            return "Solo puede contener numeros"
        return None