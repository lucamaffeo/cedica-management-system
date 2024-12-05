from src.core.validation.validator import Validator, MaxLength
from src.core.validation.rules.numbers import OnlyNumbers
from src.core.validation.rules.date import dateFormat

class ArticleValidator(Validator):
    def __init__(self):
        super().__init__()

        # author validation
        self.add_rule('author', MaxLength(255))

        # date validation
        self.add_rule('published_from', dateFormat())
        self.add_rule('published_to', dateFormat())

    def validate_request(self, data):
        return self.validate(data)