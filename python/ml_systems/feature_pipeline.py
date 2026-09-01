"""Point-in-time feature storage for ML systems interview practice."""

from __future__ import annotations

from copy import deepcopy
from dataclasses import dataclass
from math import isfinite
from typing import Any, Mapping


@dataclass(frozen=True)
class FeatureEvent:
    entity_id: str
    feature: str
    timestamp_ms: int
    value: Any


class FeaturePipeline:
    """Validate feature events and serve latest values at an as-of cutoff."""

    def __init__(self, schema: Mapping[str, type]) -> None:
        if not schema or any(not isinstance(name, str) or not name for name in schema):
            raise ValueError("schema must contain named features")
        if any(not isinstance(kind, type) for kind in schema.values()):
            raise ValueError("schema values must be types")
        self.schema = dict(schema)
        self._events: dict[str, dict[str, list[FeatureEvent]]] = {}

    def ingest(self, entity_id: str, feature: str, timestamp_ms: int, value: Any) -> FeatureEvent:
        if not isinstance(entity_id, str) or not entity_id:
            raise ValueError("entity_id must be a non-empty string")
        if feature not in self.schema:
            raise ValueError(f"unknown feature: {feature}")
        if not isinstance(timestamp_ms, int) or isinstance(timestamp_ms, bool) or timestamp_ms < 0:
            raise ValueError("timestamp_ms must be a non-negative integer")
        expected = self.schema[feature]
        if (
            not isinstance(value, expected)
            or (expected is int and isinstance(value, bool))
            or (expected is float and not isfinite(value))
        ):
            raise TypeError(f"{feature} must have type {expected.__name__}")
        event = FeatureEvent(entity_id, feature, timestamp_ms, deepcopy(value))
        feature_events = self._events.setdefault(entity_id, {}).setdefault(feature, [])
        feature_events.append(event)
        feature_events.sort(key=lambda item: item.timestamp_ms)
        return event

    def snapshot(self, entity_id: str, as_of_ms: int, features: list[str] | None = None) -> dict[str, Any]:
        if not isinstance(as_of_ms, int) or isinstance(as_of_ms, bool) or as_of_ms < 0:
            raise ValueError("as_of_ms must be a non-negative integer")
        requested = list(self.schema) if features is None else list(features)
        if any(feature not in self.schema for feature in requested):
            raise ValueError("requested feature is not in schema")
        result: dict[str, Any] = {}
        for feature in requested:
            values = self._events.get(entity_id, {}).get(feature, [])
            eligible = [event for event in values if event.timestamp_ms <= as_of_ms]
            if eligible:
                result[feature] = deepcopy(eligible[-1].value)
        return result

    lookup = snapshot
