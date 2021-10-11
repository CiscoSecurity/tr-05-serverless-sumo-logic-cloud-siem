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

INDICATOR = "indicator"
PRODUCER = "Sumo Logic"

INDICATOR_DEFAULTS = {
    "producer": PRODUCER,
    "schema_version": SCHEMA,
    "type": INDICATOR
}


def source_uri(uri_path):
    host = current_app.config["HOST"]
    return (
        f"https://{host.replace('api', 'service')}/"
        f"sec/{uri_path}"
    )


class SightingOfInsight:
    _uri_path = "insight/{id}"

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
            "source_uri": source_uri(
                self._uri_path.format(id=insight.get("id"))
            ),
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


class Indicator:
    _uri_path = "content/rules/rule/{rule_id}"

    @staticmethod
    def _transient_id(signal):
        rule_id = signal.get("ruleId")
        seeds = f"{INDICATOR}-{PRODUCER}-{rule_id}"
        return f"{INDICATOR}-{uuid5(NAMESPACE_X500, seeds)}"

    @staticmethod
    def _valid_time(signal):
        return {
            "start_time": signal.get("timestamp")
        }

    @staticmethod
    def _external_references(signal):
        rule_id = signal.get("ruleId")
        return {
            "source_name": SOURCE,
            "description": signal.get("description"),
            "url": source_uri(
                Indicator._uri_path.format(rule_id=signal.get("ruleId"))
            ),
            "external_id": rule_id
        }

    def extract(self, signal):
        return {
            "id": self._transient_id(signal),
            "valid_time": self._valid_time(signal),
            "external_references": self._external_references(signal),
            "severity": signal.get("severity", "Unknown"),
            "short_description": signal.get("description"),
            "source_uri": source_uri(
                self._uri_path.format(rule_id=signal.get("ruleId"))
            ),
            "tags": signal.get("tags"),
            **INDICATOR_DEFAULTS
        }
