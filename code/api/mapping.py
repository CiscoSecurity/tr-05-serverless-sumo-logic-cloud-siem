from uuid import uuid5, NAMESPACE_X500

from flask import current_app

SIGNAL_SEVERITY = {
    "HIGH": "High",
    "MEDIUM": "Medium",
    "LOW": "Low"
}

ENTITY_TYPES = {
    "_hostname": "hostname",
    "_ip": "ip",
    "_username": "user"
}

COUNT = 1
INTERNAL = True
SCHEMA = "1.1.8"
CONFIDENCE = "High"
SIGHTING = "sighting"
SOURCE = "Sumo Logic Cloud SIEM Enterprise"
TITLE = (
    "A Sumo Logic Cloud SIEM Insight "
    "contains observable in a Signal"
)

SIGHTING_DEFAULTS = {
    "schema_version": SCHEMA,
    "type": SIGHTING,
    "title": TITLE,
    "count": COUNT,
    "source": SOURCE,
    "internal": INTERNAL,
    "confidence": CONFIDENCE,
}


class SightingOfInsight:

    @staticmethod
    def _transient_id(insight, value) -> str:
        _id = insight.get("id")
        timestamp = insight.get("created")
        seeds = f"{SIGHTING}-{TITLE}-{timestamp}-{value}-{_id}"
        return f"{SIGHTING}-{uuid5(NAMESPACE_X500, seeds)}"

    @staticmethod
    def _short_description(insight):
        signals = insight.get("signals", [])
        unique_signals = set(signal.get("ruleId") for signal in signals)

        return (
            f"Signal: {insight.get('readableId')}-{insight.get('name')} "
            f"for entity {insight.get('entity').get('value')} "
            "contains the observable. "
            f"{len(unique_signals)} unique signals of {len(signals)} total."
        )

    @staticmethod
    def _severity(insight):
        return \
            SIGNAL_SEVERITY.get(insight.get("severity"), "Unknown")

    @staticmethod
    def _source_uri(insight):
        host = current_app.config["HOST"]
        return (
            f"https://{host.replace('api', 'service')}/"
            f"sec/insight/{insight.get('id')}"
        )

    @staticmethod
    def _observed_time(insight):
        observed_time = {
            "start_time": insight.get("created")
        }
        return observed_time

    @staticmethod
    def _target(entity, timestamp):
        _type = entity.get("entityType")

        if _type not in ENTITY_TYPES:
            return None

        target = {
            "observables": [
                {
                    "type": ENTITY_TYPES[_type],
                    "value": entity.get("value")
                }
            ],
            "observed_time": {
                "start_time": timestamp
            },
            "type": "Entity"
        }

        return target

    def extract(self, insight, observable):

        sighting = {
            "id": self._transient_id(insight, observable["value"]),
            "observed_time": self._observed_time(insight),
            "description": insight.get("description") or "",
            "external_ids": [insight.get("id"), insight.get("readableId")],
            "observables": [observable] if observable else [],
            "resolution": insight.get("resolution") or "Unresolved",
            "severity": self._severity(insight),
            "short_description": self._short_description(insight),
            "source_uri": self._source_uri(insight),
            **SIGHTING_DEFAULTS
        }

        entity = insight.get("entity")
        if entity:
            target = self._target(entity, insight.get("timestamp"))
            sighting["targets"] = [target]

        closed = insight.get("closed")
        if closed:
            sighting["observed_time"]["end_time"] = closed

        return sighting
