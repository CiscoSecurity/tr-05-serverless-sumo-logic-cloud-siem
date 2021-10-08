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
from api.errors import MoreInsightsAvailableWarning


DEFAULT_LIMIT = 10


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

    def get_insights(self, observable):
        params = {'q': observable, 'limit': self._limit}
        response = self._request(path='insights', params=params)
        data = response['data']

        if data['total'] > DEFAULT_LIMIT:
            add_error(MoreInsightsAvailableWarning(observable))

        return data['objects']
