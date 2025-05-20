from typing import Dict, Any, List
from src.core.validation.rules.date import dateFormat
from src.core.validation.validator import ValidationError, Validator, Required, MaxLength
from src.core.validation.rules.payment import ValidAmount, ValidPaymentType
from src.core.validation.rules.numbers import OnlyNumbers
from src.core.repositories import employee
from src.core.validation.rules.beneficiary import BeneficiaryExists


class PaymentValidator(Validator):
    def __init__(self):
        super().__init__()

        # Amount validation
        self.add_rule('amount', Required())
        self.add_rule('amount', ValidAmount())

        # Payment type validation
        self.add_rule('type', Required())
        self.add_rule('type', ValidPaymentType())

        self.add_rule('date', dateFormat())

        # Description validation (optional but with max length)
        self.add_rule('description', MaxLength(500))

        # Beneficiary ID validation
        self.add_rule('beneficiary_id', OnlyNumbers())
        self.add_rule('beneficiary_id', Required())
        self.add_rule('beneficiary_id', BeneficiaryExists())

    def validate_create(self, data: Dict[str, Any]) -> List[ValidationError]:
        """
        Validate data for payment creation
        Additional validations specific to creation can be added here
        """
        if data.get('type') != 'Honorarios':
            self.rules.pop('beneficiary_id',Required)
            self.rules.pop('beneficiary_id',BeneficiaryExists)
        return self.validate(data)

    def validate_update(self, data: Dict[str, Any], payment_id: int) -> List[ValidationError]:
        """
        Validate data for payment update
        Additional validations specific to updates can be added here
        """
        if data.get('type') != 'Honorarios':
            self.rules.pop('beneficiary_id',Required)
            self.rules.pop('beneficiary_id',BeneficiaryExists)
        return self.validate(data)
