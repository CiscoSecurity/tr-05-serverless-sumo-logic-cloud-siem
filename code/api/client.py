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
DEFAULT_LIMIT = 10


class SumoLogicCloudSIEMClient:

    def __init__(self, credentials):
        self._credentials = credentials
        self._headers = {
            'User-Agent': current_app.config['USER_AGENT']
        }
        self._ctr_limit = current_app.config['CTR_ENTITIES_LIMIT']
        self._insights = []

    def _url(self, api_path):
        url = current_app.config['CLOUD_SIEM_API_ENDPOINT']
        return url.format(host=self._credentials.get('host'),
                          api_path=api_path)

    @property
    def _auth(self):
        return (self._credentials.get('access_id'),
                self._credentials.get('access_key'))

    @property
    def _limit(self):
        # limits logic will probably be changed after Michael's clarifications
        return self._ctr_limit if self._ctr_limit <= DEFAULT_LIMIT \
            else DEFAULT_LIMIT

    def _request(self, path, method='GET', body=None, params=None,
                 api_path='api/sec/v1'):
        url = '/'.join([self._url(api_path), path.lstrip('/')])

        try:
            response = requests.request(method, url, json=body, params=params,
                                        auth=self._auth, headers=self._headers)
        except SSLError as error:
            raise CloudSIEMSSLError(error)
        except UnicodeError:
            raise AuthorizationError(INVALID_CREDENTIALS)
        except (ConnectionError, MissingSchema, InvalidSchema, InvalidURL):
            raise CloudSIEMConnectionError(self._url(api_path))

        if response.ok:
            return response.json()

        raise CriticalCloudSIEMResponseError(response)

    def health(self):
        return self._request(path='healthEvents',
                             params={'limit': 1},
                             api_path='api/v1')

    def get_insights(self, observable, offset=0):
        params = {'q': observable, 'limit': self._limit, 'offset': offset}
        response = self._request(path='insights', params=params)
        data = response['data']

        self._insights.extend(data['objects'])

        if data['hasNextPage'] and len(self._insights) < self._ctr_limit:
            self.get_insights(observable, offset+self._limit)

        return self._insights
