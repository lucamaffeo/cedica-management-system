from typing import Dict, Any, List, Optional
from dataclasses import dataclass
from abc import ABC, abstractmethod

@dataclass
class ValidationError:
    field: str
    message: str

class ValidationRule(ABC):
    @abstractmethod
    def validate(self, value: Any) -> Optional[str]:
        pass

class Required(ValidationRule):
    def validate(self, value: Any) -> Optional[str]:
        if not value or (isinstance(value, str) and not value.strip()):
            return "Este campo es obligatorio"
        return None

class MinLength(ValidationRule):
    def __init__(self, min_length: int):
        self.min_length = min_length

    def validate(self, value: str) -> Optional[str]:
        if len(str(value)) < self.min_length:
            return f"La longitud mínima es de {self.min_length} caracteres"
        return None

class MaxLength(ValidationRule):
    def __init__(self, max_length: int):
        self.max_length = max_length

    def validate(self, value: str) -> Optional[str]:
        if len(str(value)) > self.max_length:
            return f"La longitud máxima es de {self.max_length} caracteres"
        return None

class Validator:
    def __init__(self):
        self.rules: Dict[str, List[ValidationRule]] = {}

    def add_rule(self, field: str, rule: ValidationRule) -> 'Validator':
        if field not in self.rules:
            self.rules[field] = []
        self.rules[field].append(rule)
        return self

    def validate(self, data: Dict[str, Any]) -> List[ValidationError]:
        errors: List[ValidationError] = []

        for field, rules in self.rules.items():
            value = data.get(field)
            for rule in rules:
                if error_message := rule.validate(value):
                    errors.append(ValidationError(field, error_message))
                    break  # Dejar de comprobar otras reglas para este campo una vez que una falla

        return errors
