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
from api.mapping import Sighting


enrich_api = Blueprint('enrich', __name__)

get_observables = partial(get_json, schema=ObservableSchema(many=True))


@enrich_api.route('/observe/observables', methods=['POST'])
def observe_observables():
    key = get_credentials()
    observables = get_observables()
    client = SumoLogicCloudSIEMClient(key)

    sighting_map = Sighting()

    g.sightings = []

    for observable in observables:
        insights = client.get_insights(observable['value'])
        for insight in insights:

            insight_sighting = \
                sighting_map.extract_from_insight(insight, observable)
            g.sightings.append(insight_sighting)

            for signal in client.get_signals_from_insight(insight):
                signal_sighting = \
                    sighting_map.extract_from_signal(signal,
                                                     observable,
                                                     insight)
                g.sightings.append(signal_sighting)

        signals = client.get_signals(observable['value'])
        for signal in signals:

            signal_sighting = \
                sighting_map.extract_from_signal(signal, observable)
            g.sightings.append(signal_sighting)

    return jsonify_result()


@enrich_api.route('/refer/observables', methods=['POST'])
def refer_observables():
    _ = get_credentials()
    _ = get_observables()
    return jsonify_data([])
