from ..validator import ValidationRule


class LinkFormat(ValidationRule):
    def validate(self, value: str) -> str | None:
        if not value:
            return None
        if not value.startswith('http'):
            return "El enlace debe comenzar con 'http'"
        return None
