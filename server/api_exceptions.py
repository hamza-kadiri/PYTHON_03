def invalid_fields_to_dict(invalid_fields):
    final = {}
    for invalid_field in invalid_fields:
        final = {**final, **(invalid_field.to_dict())}
    return final


class InvalidField:
    def __init__(self, field: str, error: str):
        self.field = field
        self.error = error

    def to_dict(self):
        return {self.field: self.error}


class ExceptionWithInvalidFields(Exception):

    def __init__(self, invalid_fields: [InvalidField] = []):
        self._invalid_fields = invalid_fields

    @property
    def invalid_fields(self):
        return invalid_fields_to_dict(self._invalid_fields)


class InvalidForm(ExceptionWithInvalidFields):
    status_code = 400
    error_message = "Invalid Fields"

    def __init__(self, invalid_fields: [InvalidField] = []):
        ExceptionWithInvalidFields.__init__(self, invalid_fields)


class InvalidAuth(ExceptionWithInvalidFields):
    status_code = 400
    error_message = "Invalid username or password"

    def __init__(self):
        invalid_fields = [InvalidField("username", ""), InvalidField("password", "")]
        ExceptionWithInvalidFields.__init__(self, invalid_fields)


class InvalidDBOperation(ExceptionWithInvalidFields):
    status_code = 403

    def __init__(self, error_message: str, invalid_fields: [InvalidField] = []):
        ExceptionWithInvalidFields.__init__(self, invalid_fields)
        self.error_message = error_message
