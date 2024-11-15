from http import HTTPStatus

from src.resources import strings


class BaseError(Exception):
    def __init__(self, status_code: int, message: str):
        self.status_code = status_code
        self.message = message
        super().__init__(self.message)


class NotFoundError(BaseError):
    def __init__(self, resource: str):
        super().__init__(HTTPStatus.NOT_FOUND, strings.ERR_NOT_FOUND.format(resource=resource))


class BadRequestError(BaseError):
    def __init__(self, details: str):
        super().__init__(HTTPStatus.BAD_REQUEST, strings.ERR_BAD_REQUEST.format(details=details))
