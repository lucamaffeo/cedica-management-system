import re
from ..validator import ValidationRule


class DNIFormat(ValidationRule):
    def validate(self, value: str) -> str | None:
        if not value:
            return None
        pattern = r'^\d{1,3}(\.\d{3}){1,3}$'
        pattern2 = r'^\d{1,9}$'
        if not (re.match(pattern, value) or re.match(pattern2, value)):
            return "Formato de DNI inválido"
        return None
