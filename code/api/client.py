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


class SumoLogicCloudSIEMClient:

    def __init__(self, credentials):
        self._credentials = credentials
        self._headers = {
            'User-Agent': current_app.config['USER_AGENT']
        }
        self.ctr_limit = \
            current_app.config['CTR_ENTITIES_LIMIT']

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
            """We receive this exception when user
            inputs cyrillic in credentials"""
            raise CriticalCloudSIEMResponseError(HTTPStatus.UNAUTHORIZED)
        except (ConnectionError, MissingSchema, InvalidSchema, InvalidURL):
            """We receive IncalidURL exception when user
            leaves host value empty"""
            raise CloudSIEMConnectionError(self._url(api_path))

        if response.ok:
            return response.json()

        raise CriticalCloudSIEMResponseError(response.status_code,
                                             response.text,
                                             url)

    def health(self):
        return self._request(path='healthEvents',
                             params={'limit': 1},
                             api_path='api/v1')

    def get_insights(self, observable, limit=10):
        if self.ctr_limit <= limit:
            limit = self.ctr_limit

        params = {'q': observable, 'limit': limit}
        response = self._request(path='insights', params=params)
        data = response['data']

        if data['total'] > limit:
            add_error(MoreInsightsAvailableWarning(observable))

        return data['objects']

    def get_signals(self, observable, limit):

        params = {'q': observable, 'limit': limit}
        response = self._request(path='signals', params=params)
        data = response['data']

        if data['total'] > limit:
            add_error(MoreSignalsAvailableWarning(observable))

        return data['objects']

    @staticmethod
    def get_insights_signals(insights, observable):
        signals = []
        for insight in insights:
            for signal in insight.get('signals'):
                signal['entity'] = insight['entity']
                if observable in str(signal) and signal not in signals:
                    signals.append(signal)
        return signals
