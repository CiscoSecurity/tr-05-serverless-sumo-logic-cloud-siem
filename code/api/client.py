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
SIGNALS_DEFAULT_LIMIT = 100


class SumoLogicCloudSIEMClient:

    def __init__(self, credentials):
        self._credentials = credentials
        self._headers = {
            'User-Agent': current_app.config['USER_AGENT']
        }
        self._ctr_limit = \
            current_app.config['CTR_ENTITIES_LIMIT']
        self._default_ctr_limit = \
            current_app.config['CTR_DEFAULT_ENTITIES_LIMIT']

    def _url(self, api_path):
        url = current_app.config['CLOUD_SIEM_API_ENDPOINT']
        return url.format(host=self._credentials.get('host'),
                          api_path=api_path)

    @property
    def _auth(self):
        return (self._credentials.get('access_id'),
                self._credentials.get('access_key'))

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
        limit = 10
        if self._ctr_limit <= limit:
            limit = self._ctr_limit

        params = {'q': observable, 'limit': limit}
        response = self._request(path='insights', params=params)
        data = response['data']

        if data['total'] > limit:
            add_error(MoreInsightsAvailableWarning(observable))

        return data['objects']

    def get_signals(self, observable):
        limit = self._ctr_limit - len(g.sightings)

        params = {'q': observable, 'limit': limit}
        response = self._request(path='signals', params=params)
        data = response['data']

        if data['total'] > self._default_ctr_limit:
            add_error(MoreSignalsAvailableWarning(observable))

        return data['objects']

    @staticmethod
    def get_signals_from_insight(insight):
        signals = []
        for signal in insight['signals']:
            if signal not in signals:
                signals.append(signal)

        return signals
