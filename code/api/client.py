import requests
from flask import current_app, g
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
from api.utils import add_error
from api.errors import (
    MoreInsightsAvailableWarning,
    MoreSignalsAvailableWarning
)


INVALID_CREDENTIALS = 'wrong access_id or access_key'
DEFAULT_LIMIT = 10

INSIGHTS_DEFAULT_LIMIT = 10
SIGNALS_DEFAULT_LIMIT = 100


class SumoLogicCloudSIEMClient:

    def __init__(self, credentials):
        self._credentials = credentials
        self._headers = {
            'User-Agent': current_app.config['USER_AGENT']
        }
        self._ctr_limit = current_app.config['CTR_ENTITIES_LIMIT']

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
        return self._ctr_limit if \
            self._ctr_limit <= INSIGHTS_DEFAULT_LIMIT else \
            INSIGHTS_DEFAULT_LIMIT


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

    def get_insights(self, observable):
        params = {'q': observable, 'limit': self._limit}
        response = self._request(path='insights', params=params)
        data = response['data']

        if data['total'] > INSIGHTS_DEFAULT_LIMIT:
            add_error(MoreInsightsAvailableWarning(observable))

        return data['objects']

    def get_signals(self, observable):
        params = {'q': observable, 'limit': self._limit - len(g.sightings)}
        response = self._request(path='signals', params=params)
        data = response['data']

        if data['total'] > SIGNALS_DEFAULT_LIMIT:
            add_error(MoreSignalsAvailableWarning(observable))

        return data['objects']
