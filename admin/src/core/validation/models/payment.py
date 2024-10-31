from typing import Dict, Any, List
from src.core.validation.validator import ValidationError, Validator, Required, MaxLength
from src.core.validation.rules.payment import ValidAmount, ValidPaymentType

class PaymentValidator(Validator):
    def __init__(self):
        super().__init__()

        # Amount validation
        self.add_rule('amount', Required())
        self.add_rule('amount', ValidAmount())

        # Payment type validation
        self.add_rule('type', Required())
        self.add_rule('type', ValidPaymentType())

        # Description validation (optional but with max length)
        self.add_rule('description', MaxLength(500))

    def validate_create(self, data: Dict[str, Any]) -> List[ValidationError]:
        """
        Validate data for payment creation
        Additional validations specific to creation can be added here
        """
        return self.validate(data)

    def validate_update(self, data: Dict[str, Any], payment_id: int) -> List[ValidationError]:
        """
        Validate data for payment update
        Additional validations specific to updates can be added here
        """
        return self.validate(data)

# Example usage:
"""
validator = PaymentValidator()

# Example data
payment_data = {
    'amount': '1000.50',
    'type': 'Honorarios',
    'description': 'Pago mensual',
}

# Validate
errors = validator.validate_create(payment_data)
if errors:
    for error in errors:
        print(f"{error.field}: {error.message}")
"""
