from src.core.validation.rules.date import dateFormat
from src.core.validation.rules.payment_method import ValidPaymentMethod
from src.core.validation.rules.char_special import OnlyLettersWithSpecialChars
from src.core.validation.rules.job_position import ValidJobPosition
from src.core.validation.rules.dni import DNIFormat
from src.core.validation.validator import Validator, MaxLength
from src.core.validation.rules.letters import OnlyLetters
from src.core.validation.rules.numbers import OnlyNumbers


class ReportValidator(Validator):
    def __init__(self):
        super().__init__()

    def validate_report(self, data):
        return self.validate(data)

    def validate_AntiguedadEmpleados(self, data):
        self.add_rule('search', OnlyLetters())  # Verificar que 'search' contenga solo letras
        self.add_rule('search', MaxLength(30))  # Limitar a un máximo de 30 caracteres
        self.add_rule('job_position', OnlyLettersWithSpecialChars())  
        
        # Lista de puestos laborales
        job_positions = [
            'Administrativo/a', 'Terapeuta', 'Conductor', 'Auxiliar de pista', 
            'Herrero', 'Veterinario', 'Entrenador de Caballos', 'Domador', 
            'Profesor de Equitación', 'Docente de Capacitación', 
            'Auxiliar de mantenimiento', 'Otro'
        ]
        
        self.add_rule('job_position', ValidJobPosition(job_positions))
        self.add_rule('job_position', MaxLength(30)) 

        # Validar otros campos
        self.add_rule('min_seniority', OnlyNumbers())
        self.add_rule('max_seniority', OnlyNumbers())

        self.add_rule('start_date', dateFormat())
        
        return self.validate(data)

    def validate_receipt_payment_method_report(self, data):
        payment_methods = [
        'Todos los Medios de Pago','Efectivo', 'Tarjeta de Crédito', 'Tarjeta de Débito', 'Transferencia', 'Otro'
        ]

        self.add_rule('payment_method', OnlyLettersWithSpecialChars()) 
        self.add_rule('payment_method', MaxLength(30))
        self.add_rule('payment_method', ValidPaymentMethod(payment_methods))
        self.add_rule('min_receipts', OnlyNumbers())
        self.add_rule('max_receipts', OnlyNumbers())
        self.add_rule('min_quantity', OnlyNumbers())
        self.add_rule('max_quantity', OnlyNumbers())
        return self.validate(data)

    def validate_riders_by_age(self, data):
        self.add_rule('name', MaxLength(30))
        self.add_rule('name', OnlyLetters())
        self.add_rule('surname', MaxLength(30))
        self.add_rule('surname', OnlyLetters())
        self.add_rule('dni', MaxLength(20))
        self.add_rule('dni', DNIFormat())
        self.add_rule('min_age', OnlyNumbers())
        self.add_rule('max_age', OnlyNumbers())
        return self.validate(data)
