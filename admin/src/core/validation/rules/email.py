import re
from ..validator import ValidationRule

class EmailFormat(ValidationRule):
    def validate(self, value: str) -> str | None:
        if not value:
            return None
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(pattern, value):
            return "Invalid email format"
        return None
