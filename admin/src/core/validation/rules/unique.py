
from src.core.database import db as Database

class Unique:
    def __init__(self, table, column):
        self.table = table
        self.column = column

    def validate(self, value):
        db = Database()
        query = f"SELECT COUNT(*) FROM {self.table} WHERE {self.column} = %s"
        result = db.execute(query, (value,))
        if result[0][0] > 0:
            return False
        return True

    def __call__(self, value):
        return self.validate(value)