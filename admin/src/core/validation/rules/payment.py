import decimal
from typing import Optional, Any
from src.core.validation.validator import ValidationRule


class ValidAmount(ValidationRule):
    """Validates that an amount is a positive number with max 2 decimal places"""

    def validate(self, value: Any) -> Optional[str]:
        if not value:
            return None  # Let Required rule handle empty values

        try:
            # Check if value contains only numbers and commas
            if not all(char.isdigit() or char == ',' for char in str(value)):
                return "El monto debe contener solo números y comas"

            # Remove commas from the value
            value = str(value).replace(',', '')
            amount = decimal.Decimal(value)
            if amount <= 0:
                return "El monto debe ser mayor a 0"

            # Check decimal places
            decimal_places = abs(int(amount.as_tuple().exponent))
            if decimal_places > 2:
                return "El monto no puede tener más de 2 decimales"

            if amount > 9999999.99:  # Max amount validation (adjust as needed)
                return "El monto excede el límite permitido"

        except (ValueError, decimal.InvalidOperation):
            return "El monto debe ser un número válido"

        return None


class ValidPaymentType(ValidationRule):
    """Validates that payment type is one of the allowed values"""

    def validate(self, value: Any) -> Optional[str]:
        valid_types = ['Honorarios', 'Proveedor', 'Gastos varios']
        if value not in valid_types:
            return f"El tipo de pago debe ser uno de: {', '.join(valid_types)}"
        return None
