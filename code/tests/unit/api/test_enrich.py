from http import HTTPStatus
from unittest.mock import patch

from pytest import fixture

from tests.unit.api.utils import get_headers
from tests.unit.conftest import (
    mock_api_response
)
from tests.unit.payloads_for_tests import (
    EXPECTED_RESPONSE_OF_JWKS_ENDPOINT,
    SIGNALS,
    INSIGHTS
)


def routes():
    yield '/observe/observables'
    yield '/refer/observables'


def ids():
    yield '59407741-3ef2-4244-8d5b-8332206bdb5c'
    yield '4b6e1c6c-aea6-495c-b255-0275314f6d2c'


@fixture(scope='module', params=routes(), ids=lambda route: f'POST {route}')
def route(request):
    return request.param


@fixture(scope='module')
def invalid_json_value():
    return [{'type': 'ip', 'value': ''}]


@patch('requests.get')
def test_enrich_call_with_valid_jwt_but_invalid_json_value(
        mock_request,
        route, client, valid_jwt, invalid_json_value,
        invalid_json_expected_payload
):
    mock_request.return_value = \
        mock_api_response(payload=EXPECTED_RESPONSE_OF_JWKS_ENDPOINT)
    response = client.post(route,
                           headers=get_headers(valid_jwt()),
                           json=invalid_json_value)
    assert response.status_code == HTTPStatus.OK
    assert response.json == invalid_json_expected_payload(
        "{0: {'value': ['Field may not be blank.']}}"
    )


@fixture(scope='module')
def valid_json():
    return [{'type': 'domain', 'value': 'cisco.com'}]


@patch('requests.get')
@patch('api.client.SumoLogicCloudSIEMClient.get_insights')
@patch('api.client.SumoLogicCloudSIEMClient.get_signals')
@patch('api.mapping.uuid4')
def test_enrich_call_success(mock_id, mock_signals, mock_insights,
                             mock_request, expected_relay_response, route,
                             client, valid_jwt, valid_json):
    mock_request.return_value = \
        mock_api_response(payload=EXPECTED_RESPONSE_OF_JWKS_ENDPOINT)
    mock_insights.return_value = INSIGHTS
    mock_signals.return_value = SIGNALS
    mock_id.side_effect = ids()
    response = client.post(route, headers=get_headers(valid_jwt()),
                           json=valid_json)
    assert response.status_code == HTTPStatus.OK
    assert response.json == expected_relay_response
