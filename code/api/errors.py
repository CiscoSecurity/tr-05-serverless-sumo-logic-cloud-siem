from http import HTTPStatus
from collections import defaultdict

AUTH_ERROR = 'authorization error'
INVALID_ARGUMENT = 'invalid argument'
UNKNOWN = 'unknown'
CONNECTION_ERROR = 'connection error'
INVALID_CREDENTIALS = 'wrong access_id or access_key'
URL_NOT_FOUND = 'URL {url} is not found'


class TRFormattedError(Exception):
    def __init__(self, code, message, type_='fatal'):
        super().__init__()
        self.code = code or UNKNOWN
        self.message = message or 'Something went wrong.'
        self.type_ = type_

    @property
    def json(self):
        return {'type': self.type_,
                'code': self.code,
                'message': self.message}


class AuthorizationError(TRFormattedError):
    def __init__(self, message):
        super().__init__(
            AUTH_ERROR,
            f'Authorization failed: {message}'
        )


class InvalidArgumentError(TRFormattedError):
    def __init__(self, message):
        super().__init__(
            INVALID_ARGUMENT,
            str(message)
        )


class WatchdogError(TRFormattedError):
    def __init__(self):
        super().__init__(
            code='health check failed',
            message='Invalid Health Check'
        )


class CloudSIEMSSLError(TRFormattedError):
    def __init__(self, error):
        message = getattr(
            error.args[0].reason.args[0], 'verify_message', ''
        ) or error.args[0].reason.args[0].args[0]

        super().__init__(
            UNKNOWN,
            f'Unable to verify SSL certificate: {message}'
        )


class CloudSIEMConnectionError(TRFormattedError):
    def __init__(self, url):
        super().__init__(
            CONNECTION_ERROR,
            'Unable to connect to Sumo Logic Cloud SIEM,'
            f' validate the configured API endpoint: {url}'
        )


class CriticalCloudSIEMResponseError(TRFormattedError):
    def __init__(self, status_code, response_text=None, url=None):
        status_code_map = {
            HTTPStatus.UNAUTHORIZED: INVALID_CREDENTIALS,
            HTTPStatus.NOT_FOUND: URL_NOT_FOUND.format(url=url)
        }
        status_code_map = defaultdict(lambda: response_text, status_code_map)
        super().__init__(
            HTTPStatus(status_code).phrase,
            f'Unexpected response from Sumo Logic Cloud SIEM: {status_code_map[status_code]}'
        )
