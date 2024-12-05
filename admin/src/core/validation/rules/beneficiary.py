
from typing import Any, Optional
from src.core.validation.validator import ValidationRule, ValidationError
from src.core.repositories import employee

class BeneficiaryExists(ValidationRule):
    def validate(self, value: Any) -> Optional[str]:
        if not value:
            return None
        if not employee.get_employee(value):
            return f'Beneficiary ID {value} no existe.'
        return None