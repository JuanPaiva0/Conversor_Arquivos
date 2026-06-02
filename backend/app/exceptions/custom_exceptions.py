class AppException(Exception):
    def __init__(self, message: str, status_code: int):
        self.message = message
        self.status_code = status_code
        super().__init__(message)

class ConversionError(AppException):
    def __init__(self, message: str):
        super().__init__(message, 500)

class InvalidFileExtensionError(AppException):
    def __init__(self, message: str):
        super().__init__(message, 400)

class InvalidMimeTypeError(AppException):
    def __init__(self, message: str):
        super().__init__(message, 400)

class FileTooLargeError(AppException):
    def __init__(self, message: str):
        super().__init__(message, 413)

class MissingFilenameError(AppException):
    def __init__(self, message: str):
        super().__init__(message, 400)