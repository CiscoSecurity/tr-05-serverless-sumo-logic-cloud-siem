from uuid import uuid5, NAMESPACE_X500, uuid4

from flask import current_app

INSIGHT = "insight"
SIGNAL = "signal"

INDICATOR = "indicator"
SIGHTING = "sighting"
RELATIONSHIP = "relationship"

SCHEMA = "1.1.8"
PRODUCER = "Sumo Logic"
SOURCE = "Sumo Logic Cloud SIEM Enterprise"
INSIGHT_TITLE = (
    "A Sumo Logic Cloud SIEM Insight "
    "contains observable in a Signal"
)
SIGNAL_TITLE = (
    "A Sumo Logic Cloud SIEM Signal "
    "contains observable in a Signal"
)

INSIGHT_SEVERITY = {
    "HIGH": "High",
    "MEDIUM": "Medium",
    "LOW": "Low"
}

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

CTIM_DEFAULTS = {
    'schema_version': SCHEMA
}

SIGHTING_DEFAULTS = {
    "type": SIGHTING,
    "count": 1,
    "source": SOURCE,
    "internal": True,
    "confidence": "High",
    **CTIM_DEFAULTS
}

INDICATOR_DEFAULTS = {
    "producer": PRODUCER,
    "type": INDICATOR,
    "source": SOURCE,
    **CTIM_DEFAULTS
}


def source_uri(uri_path):
    host = current_app.config["HOST"]
    return (
        f"https://{host.replace('api', 'service')}/"
        f"sec/{uri_path}"
    )


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

    def _extract_defaults(self, obj, observable, _type):
        return {
            "id": self._transient_id(obj, observable, _type),
            "observed_time": self._observed_time(obj, _type),
            "description": obj.get("description") or "",
            "observables": [observable] if observable else [],
            "severity": self._severity(obj, _type),
            **SIGHTING_DEFAULTS
        }


class SignalSighting(Sighting):
    _uri_path = "signal/{signal_id}"

    @staticmethod
    def _short_description(signal):
        return (
            f"Signal: {signal.get('name')} for entity "
            f"{signal.get('entity').get('value')} contains "
            "the observable."
        )

    def extract(self, signal, observable):
        signal_id = signal.get("id")
        sighting = {
            "external_ids": [signal_id],
            "title": SIGNAL_TITLE,
            "short_description": self._short_description(signal),
            "source_uri": source_uri(
                self._uri_path.format(signal_id=signal_id)
            ),
            **self._extract_defaults(signal, observable, SIGNAL),
        }

        entity = signal.get("entity")
        if entity:
            target = self._target(entity, signal.get("timestamp"))
            sighting["targets"] = [target]

        return sighting


class InsightSighting(Sighting):
    _uri_path = "insight/{insight_id}"

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

    def extract(self, insight, observable):
        insight_id = insight.get("id")
        sighting = {
            "external_ids": [insight_id, insight.get("readableId")],
            "resolution": insight.get("resolution") or "Unresolved",
            "title": INSIGHT_TITLE,
            "short_description": self._short_description(insight),
            "source_uri": source_uri(
                self._uri_path.format(insight_id=insight_id)
            ),
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
            "external_references": [self._external_references(signal)],
            "severity": SIGNAL_SEVERITY.get(signal.get("severity"), "Unknown"),
            "short_description": signal.get("description"),
            "source_uri": source_uri(
                self._uri_path.format(rule_id=signal.get("ruleId"))
            ),
            "tags": signal.get("tags"),
            **INDICATOR_DEFAULTS
        }


class Relationship:

    @staticmethod
    def extract(source_ref, target_ref, type_):
        return {
            'id': f'transient:{RELATIONSHIP}-{uuid4()}',
            'source_ref': source_ref,
            'target_ref': target_ref,
            'relationship_type': type_,
            'type': RELATIONSHIP,
            **CTIM_DEFAULTS
        }
