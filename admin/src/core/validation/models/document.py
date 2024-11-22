from src.core.validation.validator import Validator, Required, MaxLength, In
from src.core.validation.rules.link import LinkFormat
from src.core.validation.rules.file import FileExtension


class DocumentValidator(Validator):
    def __init__(self):
        super().__init__()

        # Definir las categorías del enum
        document_type_categories = [
            'Entrevista', 'Evaluación', 'Planificaciones', 'Evolución', 'Crónicas', 'Documental',
            'Ficha general del caballo', 'Planificación de Entrenamiento', 'Informe de Evolución',
            'Carga de Imágenes', 'Registro veterinario', 'Otro'
        ]
        valid_file_extensions = ["jpeg", "jpg", "xls", "pdf", "doc", "docx"]

        # title validation
        self.add_rule('title', Required())
        self.add_rule('title', MaxLength(50))

        # document type validation
        self.add_rule('document_type', Required())
        self.add_rule('document_type', In(document_type_categories))

        # Description validation (optional but with max length)
        self.add_rule('description', MaxLength(500))

        # entity validation
        self.add_rule('entity_id', Required())

        # entity type
        self.add_rule('entity_type', Required())
        self.add_rule('entity_type', In(['riders', 'employees', 'horses']))

        # link validator. Solo valida cuando se envía un documento de tipo link
        self.add_rule('link', LinkFormat())

        # filename validation. Solo valida cuando se envía un documento de tipo file
        self.add_rule('filename', FileExtension(valid_file_extensions))

    def validate_create(self, data):
        return self.validate(data)
