import re
from ..validator import ValidationRule


class dateFormat(ValidationRule):
    def validate(self, value: str) -> str | None:
        if not value:
            return None
        pattern = r'^\d{1,4}-\d{2}-\d{2}$|^\d{1,4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z$'
        if not re.match(pattern, value):
            return "Formato de fecha inválido"
        return None

