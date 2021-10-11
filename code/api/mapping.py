from uuid import uuid5, NAMESPACE_X500

from flask import current_app

INSIGHT = "insight"
INSIGHT_SEVERITY = {
    "HIGH": "High",
    "MEDIUM": "Medium",
    "LOW": "Low"
}

SIGNAL = "signal"
SIGNAL_SEVERITY = {
    1: "Low",
    2: "Low",
    3: "Low",
    4: "Medium",
    5: "Medium",
    6: "Medium",
    7: "High",
    8: "High",
    9: "High",
    10: "Critical"
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
INSIGHT_TITLE = (
    "A Sumo Logic Cloud SIEM Insight "
    "contains observable in a Signal"
)
SIGNAL_TITLE = (
    "A Sumo Logic Cloud SIEM Signal "
    "contains observable in a Signal"
)

SIGHTING_DEFAULTS = {
    "schema_version": SCHEMA,
    "type": SIGHTING,
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


class Sighting:

    @staticmethod
    def _transient_id(obj, value, _type) -> str:
        _id = obj.get("id")
        timestamp = obj.get("created")
        title = INSIGHT_TITLE if _type == INSIGHT else SIGNAL_TITLE
        seeds = f"{SIGHTING}-{title}-{timestamp}-{value}-{_id}"
        return f"{SIGHTING}-{uuid5(NAMESPACE_X500, seeds)}"

    @staticmethod
    def _severity(obj, _type):
        severity = {
            INSIGHT: INSIGHT_SEVERITY,
            SIGNAL: SIGNAL_SEVERITY
        }
        return severity.get(_type).get(obj.get("severity"), "Unknown")

    @staticmethod
    def _source_uri(obj, _type):
        host = current_app.config["HOST"]
        return (
            f"https://{host.replace('api', 'service')}/"
            f"sec/{_type}/{obj.get('id')}"
        )

    @staticmethod
    def _observed_time(obj, _type):
        times = {
            SIGNAL: lambda: obj.get("timestamp"),
            INSIGHT: lambda: obj.get("created")
        }
        return {"start_time": times.get(_type)()}

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

    @staticmethod
    def _insight_short_description(insight):
        signals = insight.get("signals", [])
        unique_signals = set(signal.get("ruleId") for signal in signals)

        return (
            f"Signal: {insight.get('readableId')}-{insight.get('name')} "
            f"for entity {insight.get('entity').get('value')} "
            "contains the observable. "
            f"{len(unique_signals)} unique signals of {len(signals)} total."
        )

    @staticmethod
    def _signal_short_description(signal):
        return (
            f"Signal: {signal.get('name')} for entity "
            f"{signal.get('entity').get('value')} contains "
            "the observable."
        )

    def _extract_defaults(self, obj, observable, _type):
        return {
            "id": self._transient_id(obj, observable, _type),
            "observed_time": self._observed_time(obj, _type),
            "description": obj.get("description") or "",
            "observables": [observable] if observable else [],
            "severity": self._severity(obj, _type),
            "source_uri": self._source_uri(obj, _type),
            **SIGHTING_DEFAULTS
        }


class SignalSighting(Sighting):

    def extract(self, signal, observable, insight=None):
        sighting = {
            "external_ids": [signal.get("id")],
            "title": SIGNAL_TITLE,
            "short_description": (
                self._signal_short_description(signal) if not insight
                else self._signal_short_description(insight)
            ),
            **self._extract_defaults(signal, observable, SIGNAL),
        }

        entity = (
            signal.get("entity") if not insight
            else insight.get("entity")
        )
        if entity:
            target = self._target(entity, signal.get("timestamp"))
            sighting["targets"] = [target]

        return sighting


class InsightSighting(Sighting):

    def extract(self, insight, observable):

        sighting = {
            "external_ids": [insight.get("id"), insight.get("readableId")],
            "resolution": insight.get("resolution") or "Unresolved",
            "title": INSIGHT_TITLE,
            "short_description": self._insight_short_description(insight),
            **self._extract_defaults(insight, observable, INSIGHT),
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
    def _url(rule_id):
        host = current_app.config["HOST"]
        return (
            f"https://{host.replace('api', 'service')}/"
            f"sec/content/rules/rule/{rule_id}"
        )

    @staticmethod
    def _external_references(signal):
        rule_id = signal.get("ruleId")
        return {
            "source_name": SOURCE,
            "description": signal.get("description"),
            "url": Indicator._url(rule_id),
            "external_id": rule_id
        }

    def extract(self, signal):
        return {
            "id": self._transient_id(signal),
            "valid_time": self._valid_time(signal),
            "external_references": self._external_references(signal),
            "severity": signal.get("severity", "Unknown"),
            "short_description": signal.get("description"),
            "source_uri": self._url(signal.get("ruleId")),
            "tags": signal.get("tags"),
            **INDICATOR_DEFAULTS
        }
