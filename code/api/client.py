import requests
from flask import current_app
from requests.exceptions import (
    ConnectionError,
    MissingSchema,
    InvalidSchema,
    InvalidURL,
    SSLError
)

from api.errors import (
    AuthorizationError,
    CloudSIEMConnectionError,
    CriticalCloudSIEMResponseError,
    CloudSIEMSSLError
)

INVALID_CREDENTIALS = 'wrong access_id or access_key'


class SumoLogicCloudSIEMClient:
    def __init__(self, credentials):
        self._credentials = credentials
        self._headers = {
            'User-Agent': current_app.config['USER_AGENT']
        }

    @property
    def _url(self):
        url = current_app.config['CLOUD_SIEM_API_ENDPOINT']
        return url.format(host=self._credentials.get('host'))

    @property
    def _auth(self):
        return (self._credentials.get('access_id'),
                self._credentials.get('access_key'))

    def health(self):
        return self._request(path='signals/all')

    def _request(self, path, method="GET", body=None, params=None):
        url = '/'.join([self._url, path.lstrip('/')])

        try:
            response = requests.request(method, url, json=body, params=params,
                                        auth=self._auth, headers=self._headers)
        except SSLError as error:
            raise CloudSIEMSSLError(error)
        except UnicodeError:
            raise AuthorizationError(INVALID_CREDENTIALS)
        except (ConnectionError, MissingSchema, InvalidSchema, InvalidURL):
            raise CloudSIEMConnectionError(self._url)

        if response.ok:
            return response.json()

        raise CriticalCloudSIEMResponseError(response)
