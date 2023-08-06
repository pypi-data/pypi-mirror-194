from enum import IntEnum


class ErrorCode(IntEnum):
    SUCCESS = 0
    UNEXPECTED_ERROR = 1


class SEUtilsException(Exception):
    def __init__(
            self,
            code: int = ErrorCode.UNEXPECTED_ERROR,
            message: str = ""
    ):
        super().__init__()
        self._code = code
        self._message = message

    @property
    def code(self):
        return self._code

    @property
    def message(self):
        return self._message

    def __str__(self):
        return f"<{type(self).__name__}: (code={self.code}, message={self.message})>"


class BadCredentialsError(SEUtilsException):
    """ Raise when provided credentials are incorrect """


class SchemaValidationError(SEUtilsException):
    """ Raise when couldn't validate schema """


class SchemaParseError(SEUtilsException):
    """ Raise when couldn't parse schema file """


class MilvusInsertDataSchemaError(SEUtilsException):
    """ Raise when data fields to be inserted to milvus
        do not coincide with milvus target collection """


class ExceptionsMessage:
    BadCredentials = "provided credentials are incorrect"
