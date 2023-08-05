class A3RTTalkException(Exception):
    pass

class ApiKeyIsNull(A3RTTalkException):
    """apikey is null"""

class ApiKeyNotFound(A3RTTalkException):
    """apikey is not found"""

class DeletedAccount(A3RTTalkException):
    """deleted account"""

class TemporaryAccount(A3RTTalkException):
    """temporary account"""

class ServerNotFound(A3RTTalkException):
    """server not found"""

class ServerParameterError(A3RTTalkException):
    """server parameter error"""

class AccessDeny(A3RTTalkException):
    """access deny"""

class BadRequest(A3RTTalkException):
    """bad request"""

class NotFound(A3RTTalkException):
    """not found"""

class MethodNotAllowed(A3RTTalkException):
    """method not allowed"""

class RequestEntityTooLong(A3RTTalkException):
    """request entity too long"""

class InternalServerError(A3RTTalkException):
    """internal server error"""

class UnknownError(A3RTTalkException):
    """unknown error"""
