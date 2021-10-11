from functools import partial

from flask import Blueprint, g

from api.schemas import ObservableSchema
from api.utils import (
    get_json,
    get_credentials,
    jsonify_data,
    jsonify_result
)
from api.client import SumoLogicCloudSIEMClient
from api.mapping import SightingOfInsight, Indicator

enrich_api = Blueprint('enrich', __name__)

get_observables = partial(get_json, schema=ObservableSchema(many=True))


@enrich_api.route('/observe/observables', methods=['POST'])
def observe_observables():
    key = get_credentials()
    observables = get_observables()
    client = SumoLogicCloudSIEMClient(key)

    insight_sighting_map = SightingOfInsight()
    indicator_map = Indicator()

    g.sightings = []
    g.indicators = []

    for observable in observables:
        insights = client.get_insights(observable['value'])
        for insight in insights:

            insight_sighting = \
                insight_sighting_map.extract(insight, observable)
            g.sightings.append(insight_sighting)

            indicators = [indicator_map.extract(signal) for signal in
                          insight.get('signals')]
            g.indicators.extend(indicators)

    return jsonify_result()


@enrich_api.route('/refer/observables', methods=['POST'])
def refer_observables():
    _ = get_credentials()
    _ = get_observables()
    return jsonify_data([])
