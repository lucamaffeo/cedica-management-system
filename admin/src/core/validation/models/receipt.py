
import datetime
from typing import Dict, Any, List, Optional
from src.core.validation.rules.date import dateFormat
from src.core.validation.validator import ValidationError, ValidationRule, Validator, Required, MaxLength, In
from src.core.validation.rules.payment import ValidAmount


class DateNotInFuture(ValidationRule):
    """Validates that a date is not in the future"""

    def validate(self, value: Any) -> Optional[str]:
        if isinstance(value, str):
            try:
                value = datetime.datetime.strptime(value, '%Y-%m-%d').date()
            except ValueError:
                return "Formato de fecha inválido"
        if value > datetime.date.today():
            return "La fecha no puede ser futura"
        return None


class ReceiptValidator(Validator):
    def __init__(self):
        super().__init__()

         
        payment_method = ['Efectivo', 'Tarjeta de Crédito', 'Tarjeta de Débito',
                                'Transferencia', 'Otro']

        # Employee ID validation
        self.add_rule('employee_id', Required())

        # JA ID validation
        self.add_rule('ja_id', Required())

        # Payment date validation
        self.add_rule('payment_date', Required())
        self.add_rule('payment_date', DateNotInFuture())
        self.add_rule('payment_date', dateFormat())


        # Amount validation
        self.add_rule('quantity', Required())
        self.add_rule('quantity', ValidAmount())

        # Payment method validation
        self.add_rule('payment_method', Required())
        self.add_rule('payment_method', MaxLength(50))
        self.add_rule('payment_method', In(payment_method))

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

