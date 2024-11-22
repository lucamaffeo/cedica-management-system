import re
from ..validator import ValidationRule

class ValidJobPosition(ValidationRule):
    def __init__(self, job_positions):
        self.job_positions = job_positions

    def validate(self, value: str) -> str | None:
        if not value:
            return None
    
        if value not in self.job_positions:
            return f"El puesto laboral '{value}' no es válido. Selecciona uno de los puestos disponibles."
        return None
