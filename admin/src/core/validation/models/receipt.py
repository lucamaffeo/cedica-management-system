
from typing import Dict, Any, List
from src.core.validation.validator import ValidationError, Validator, Required, MaxLength
from src.core.validation.rules.payment import ValidAmount, ValidPaymentType

class ReceiptValidator(Validator):
    def __init__(self):
        super().__init__()

        # Employee ID validation
        self.add_rule('employee_id', Required())

        # JA ID validation
        self.add_rule('ja_id', Required())

        # Payment date validation
        self.add_rule('payment_date', Required())

        # Amount validation
        self.add_rule('quantity', Required())
        self.add_rule('quantity', ValidAmount())

        # Payment method validation
        self.add_rule('payment_method', Required())
        self.add_rule('payment_method', MaxLength(50))

        # Remarks validation (optional but with max length)
        self.add_rule('remarks', MaxLength(500))

    def validate_create(self, data: Dict[str, Any]) -> List[ValidationError]:
        """
        Validate data for receipt creation
        Additional validations specific to creation can be added here
        """
        return self.validate(data)

    def validate_update(self, data: Dict[str, Any], receipt_id: int) -> List[ValidationError]:
        """
        Validate data for receipt update
        Additional validations specific to updates can be added here
        """
        return self.validate(data)