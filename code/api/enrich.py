from functools import partial

from flask import Blueprint, g, current_app

from api.schemas import ObservableSchema
from api.utils import (
    get_json,
    get_credentials,
    jsonify_data,
    jsonify_result,
)
from api.client import SumoLogicCloudSIEMClient
from api.mapping import (
    InsightSighting,
    SignalSighting,
    Indicator,
    source_uri
)

enrich_api = Blueprint('enrich', __name__)

get_observables = partial(get_json, schema=ObservableSchema(many=True))


@enrich_api.route('/observe/observables', methods=['POST'])
def observe_observables():
    key = get_credentials()
    observables = get_observables()
    client = SumoLogicCloudSIEMClient(key)

    insight_sighting_map = InsightSighting()
    signal_sighting_map = SignalSighting()
    indicator_map = Indicator()

    g.sightings = []
    g.indicators = []

    for observable in observables:
        obs_value = observable['value']
        insights = client.get_insights(obs_value)
        for insight in insights:

            insight_sighting = \
                insight_sighting_map.extract(insight, observable)
            g.sightings.append(insight_sighting)

        insights_signals = client.get_insights_signals(insights, obs_value)

        for signal in insights_signals:
            signal_sighting = signal_sighting_map.extract(signal, observable)
            g.sightings.append(signal_sighting)

            indicator = indicator_map.extract(signal)
            g.indicators.append(indicator)

        signals = client.get_signals(obs_value, client.ctr_limit)

        for signal in signals:

            signal_sighting = signal_sighting_map.extract(signal, observable)
            if signal_sighting not in g.sightings:
                g.sightings.append(signal_sighting)

            indicator = indicator_map.extract(signal)
            if indicator not in g.indicators:
                g.indicators.append(indicator)

    return jsonify_result()


@enrich_api.route('/refer/observables', methods=['POST'])
def refer_observables():
    _ = get_credentials()
    observables = get_observables()

    obs_types_map = current_app.config['HUMAN_READABLE_OBSERVABLE_TYPES']
    relay_output = [
        {
            'id': (
                'ref-sumo-logic-search-cse-'
                f'{observable["type"].replace("_", "-")}'
                f'-{observable["value"]}'
            ),
            'title': (
                'Search for this '
                f'{obs_types_map.get(observable["type"], observable["type"])}'
            ),
            'description': (
                'Lookup this '
                f'{obs_types_map.get(observable["type"], observable["type"])}'
                ' on Sumo Logic Cloud SIEM Enterprise console'
            ),
            'url': source_uri(f'search?q={observable["value"]}'),
            'categories': ['Search', 'SumoLogic', 'Cloud SIEM Enterprise']
        }
        for observable in observables
    ]
    return jsonify_data(relay_output)
