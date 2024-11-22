import re
from ..validator import ValidationRule

class ValidPaymentMethod(ValidationRule):
    """Validates that the payment method is one of the allowed values"""

    def __init__(self, payment_methods):
        self.payment_methods = payment_methods

    def validate(self, value: str) -> str | None:
        if not value:
            return None  # Permitimos valores vacíos si no se requieren

        # Eliminar espacios adicionales
        value = value.strip()

        # Normalizamos la comparación (en caso de querer ignorar mayúsculas/minúsculas)
        normalized_payment_methods = [method.lower() for method in self.payment_methods]
        normalized_value = value.lower()

        if normalized_value not in normalized_payment_methods:
            return f"El método de pago '{value}' no es válido. Selecciona uno de los métodos disponibles."

        return None