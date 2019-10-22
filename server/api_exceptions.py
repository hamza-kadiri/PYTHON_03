class InvalidField:
    def __init__(self, field: str, error: str):
        self.field = field
        self.error = error

    def to_dict(self):
        return {"field": self.field, "error": self.error}


class InvalidForm(Exception):
    status_code = 400

    def __init__(self, invalid_fields: [InvalidField] = []):
        Exception.__init__(self)
        self.invalid_fields = invalid_fields

    def to_dict(self):
        return {"invalid_fields":[invalid_field.to_dict() for invalid_field in self.invalid_fields]}