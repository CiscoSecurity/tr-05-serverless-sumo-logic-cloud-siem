from functools import partial

from flask import Blueprint, g

from api.schemas import ObservableSchema
from api.utils import get_json, get_credentials, jsonify_data
from api.client import SumoLogicCloudSIEMClient

enrich_api = Blueprint('enrich', __name__)

get_observables = partial(get_json, schema=ObservableSchema(many=True))


@enrich_api.route('/deliberate/observables', methods=['POST'])
def deliberate_observables():
    _ = get_credentials()
    _ = get_observables()
    return jsonify_data({})


@enrich_api.route('/observe/observables', methods=['POST'])
def observe_observables():
    key = get_credentials()
    observables = get_observables()
    client = SumoLogicCloudSIEMClient(key)

    g.sightings = []

    for observable in observables:
        insights = client.get_insights(observable['value'])

    return jsonify_data({})


@enrich_api.route('/refer/observables', methods=['POST'])
def refer_observables():
    _ = get_credentials()
    _ = get_observables()
    return jsonify_data([])
