from requests import HTTPError


class NotFoundError(RuntimeError):
    def __init__(self, http_error: HTTPError):
        self.http_error = http_error


class UnauthorizedError(RuntimeError):
    def __init__(self, http_error: HTTPError):
        self.http_error = http_error
