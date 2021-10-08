from http import HTTPStatus

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


class SumoLogicCloudSIEMClient:
    def __init__(self, credentials):
        self._credentials = credentials
        self._headers = {
            'User-Agent': current_app.config['USER_AGENT']
        }

    def _url(self, api_path):
        url = current_app.config['CLOUD_SIEM_API_ENDPOINT']
        return url.format(host=self._credentials.get('host'),
                          api_path=api_path)

    @property
    def _auth(self):
        return (self._credentials.get('access_id'),
                self._credentials.get('access_key'))

    def health(self):
        return self._request(path='healthEvents',
                             params={'limit': 1},
                             api_path='api/v1')

    def _request(self, path, method='GET', body=None, params=None,
                 api_path='api/sec/v1'):
        url = '/'.join([self._url(api_path), path.lstrip('/')])

        try:
            response = requests.request(method, url, json=body, params=params,
                                        auth=self._auth, headers=self._headers)
        except SSLError as error:
            raise CloudSIEMSSLError(error)
        except UnicodeError:
            raise CriticalCloudSIEMResponseError(HTTPStatus.UNAUTHORIZED)
        except (ConnectionError, MissingSchema, InvalidSchema, InvalidURL):
            raise CloudSIEMConnectionError(self._url(api_path))

        if response.ok:
            return response.json()

        raise CriticalCloudSIEMResponseError(response.status_code, response.text, url)
