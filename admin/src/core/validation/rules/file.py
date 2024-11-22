import os
from src.core.validation.validator import ValidationRule


class FileExtension(ValidationRule):
    def __init__(self, valid_extensions):
        self.valid_extensions = valid_extensions

    def validate(self, value: str) -> str | None:
        if not value:
            return None
        _, extension = os.path.splitext(value)
        # Obtener extensión en minúsculas sin el punto
        extension = extension.lower().lstrip(".")
        if extension not in self.valid_extensions:
            return f"El archivo debe tener una de las siguientes extensiones: {', '.join(self.valid_extensions)}"
        return None
