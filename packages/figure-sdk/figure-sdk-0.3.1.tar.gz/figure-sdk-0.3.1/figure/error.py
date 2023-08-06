


class FigureError(Exception):

    def __init__(self, message=None, status=None, body=None):

        super(FigureError, self).__init__(message)
        self._message = message
        self.http_status = status
        self.body = body
        self.type = 'figure_error'

    def __unicode__(self):
        return self._message

    def __str__(self):
        return str(self).encode('utf-8')


class APIConnectionError(FigureError):

    def __init__(self, message=None, status=None, body=None):
        super(APIConnectionError, self).__init__(message, status, body)
        self.type = 'connection_error'


class BadRequestError(FigureError):

    def __init__(self, message=None, status=None, body=None):
        message = message or 'Bad Request'
        super(BadRequestError, self).__init__(message, status, body)
        self.type = 'bad_request_error'


class AuthenticationError(FigureError):

    def __init__(self, message=None, status=None, body=None):
        message = message or 'Authentication error'
        super(AuthenticationError, self).__init__(message, status, body)
        self.type = 'authentication_error'


class AuthorizationError(FigureError):

    def __init__(self, message=None, status=None, body=None):
        message = message or 'Autorization error'
        super(AuthorizationError, self).__init__(message, status, body)
        self.type = 'authorization_error'


class NotFoundError(FigureError):

    def __init__(self, message=None, status=None, body=None):
        message = message or 'Not found'
        super(NotFoundError, self).__init__(message, status, body)
        self.type = 'not_found_error'


class RateLimitError(FigureError):

    def __init__(self, message=None, status=None, body=None):
        message = message or 'Too many requests'
        super(RateLimitError, self).__init__(message, status, body)
        self.type = 'rate_limit_error'


class MethodNotAllowedError(FigureError):

    def __init__(self, message=None, status=None, body=None):
        message = message or 'Method not allowed'
        super(MethodNotAllowedError, self).__init__(message, status, body)
        self.type = 'method_not_allowed_error'


class InternalServerError(FigureError):

    def __init__(self, message=None, status=None, body=None):
        message = message or 'Internal server error'
        super(InternalServerError, self).__init__(message, status, body)
        self.type = 'internal_server_error'


class NotAvailableYetError(FigureError):

    def __init__(self, message=None, status=None, body=None):
        message = message or 'This resource is not available yet'
        super(NotAvailableYetError, self).__init__(message, status, body)
        self.type = 'not_available_yet_error'
