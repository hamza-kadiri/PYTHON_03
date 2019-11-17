class InvalidField:
    def __init__(self, field: str, error: str):
        self.field = field
        self.error = error

    def to_dict(self):
        return {self.field: self.error}


class InvalidForm(Exception):
    status_code = 400

    def __init__(self, invalid_fields: [InvalidField] = []):
        Exception.__init__(self)
        self.invalid_fields = invalid_fields

    def to_dict(self):
        final = {}
        for invalid_field in self.invalid_fields:
            final = {**final, **invalid_field.to_dict()}
        return final


class InvalidDBOperation(Exception):
    status_code = 403

    def __init__(self, error_message: str):
        Exception.__init__(self)
        self.error_message = error_message

    def to_dict(self):
        return {"error_message": self.error_message}
