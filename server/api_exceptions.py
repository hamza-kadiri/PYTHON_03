class InvalidField:
    def __init__(self, field: str, error: str):
        self.__field = field
        self.__error = error

    def to_dict(self):
        return {self.__field: self.__error}

    @property
    def field(self):
        return self.__field

    @property
    def error(self):
        return self.__error

    @staticmethod
    def invalid_fields_to_dict(invalid_fields:[InvalidField]):
        final = {}
        for invalid_field in invalid_fields:
            final = {**final, **(invalid_field.to_dict())}
        return final


class ExceptionWithInvalidFields(Exception):

    def __init__(self, status_code: int, error_message: str, invalid_fields: [InvalidField] = []):
        self.__invalid_fields = invalid_fields
        self.__status_code = status_code
        self.__error_message = error_message

    @property
    def status_code(self):
        return self.__status_code

    @property
    def error_message(self):
        return self.__error_message

    @property
    def invalid_fields(self):
        return InvalidField.invalid_fields_to_dict(self.__invalid_fields)


class InvalidForm(ExceptionWithInvalidFields):
    __status_code = 400
    __error_message = "Invalid Fields"

    def __init__(self, invalid_fields: [InvalidField] = []):
        ExceptionWithInvalidFields.__init__(self, InvalidForm.__status_code, InvalidForm.__error_message,
                                            invalid_fields)


class InvalidAuth(ExceptionWithInvalidFields):
    __status_code = 400
    __error_message = "Invalid username or password"

    def __init__(self):
        invalid_fields = [InvalidField("username", ""), InvalidField("password", "")]
        ExceptionWithInvalidFields.__init__(self, InvalidAuth.__status_code, InvalidAuth.__error_message,
                                            invalid_fields)


class InvalidDBOperation(ExceptionWithInvalidFields):
    __status_code = 403

    def __init__(self, error_message: str, invalid_fields: [InvalidField] = []):
        ExceptionWithInvalidFields.__init__(self, InvalidDBOperation.__status_code, error_message, invalid_fields)
