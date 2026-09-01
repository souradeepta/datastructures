"""A deterministic event-time tumbling-window teaching model."""

from __future__ import annotations

from dataclasses import dataclass
from copy import deepcopy
from typing import Any


@dataclass(frozen=True)
class Event:
    event_id: str
    timestamp_ms: int
    value: Any


@dataclass(frozen=True)
class WindowResult:
    start_ms: int
    end_ms: int
    events: tuple[Event, ...]

    @property
    def count(self) -> int:
        return len(self.events)

    @property
    def total(self) -> Any:
        values = [event.value for event in self.events]
        try:
            return sum(values)
        except TypeError:
            return None


class EventTimeWindows:
    """Deduplicate events and emit each finalized tumbling window once.

    Windows are half-open, ``[start, end)``, and finalize when
    ``watermark >= end + allowed_lateness_ms``. Events for finalized windows
    are retained in a late side output and do not change emitted results.
    """

    def __init__(self, window_size_ms: int, allowed_lateness_ms: int = 0) -> None:
        if not isinstance(window_size_ms, int) or isinstance(window_size_ms, bool) or window_size_ms <= 0:
            raise ValueError("window_size_ms must be positive")
        if not isinstance(allowed_lateness_ms, int) or isinstance(allowed_lateness_ms, bool) or allowed_lateness_ms < 0:
            raise ValueError("allowed_lateness_ms must be non-negative")
        self.window_size_ms = window_size_ms
        self.allowed_lateness_ms = allowed_lateness_ms
        self.watermark_ms = -1
        self._events: dict[int, list[Event]] = {}
        self._seen_ids: set[str] = set()
        self._finalized: set[int] = set()
        self._late: list[Event] = []

    def add_event(self, event_id: str, timestamp_ms: int, value: Any) -> str:
        if not isinstance(event_id, str) or not event_id:
            raise ValueError("event_id must be a non-empty string")
        if not isinstance(timestamp_ms, int) or isinstance(timestamp_ms, bool) or timestamp_ms < 0:
            raise ValueError("timestamp_ms must be a non-negative integer")
        if event_id in self._seen_ids:
            return "duplicate"
        event = Event(event_id, timestamp_ms, deepcopy(value))
        self._seen_ids.add(event_id)
        start = (timestamp_ms // self.window_size_ms) * self.window_size_ms
        if start in self._finalized:
            self._late.append(event)
            return "late"
        self._events.setdefault(start, []).append(event)
        return "accepted"

    def advance_watermark(self, watermark_ms: int) -> tuple[WindowResult, ...]:
        if not isinstance(watermark_ms, int) or isinstance(watermark_ms, bool):
            raise ValueError("watermark_ms must be an integer")
        if watermark_ms < self.watermark_ms:
            raise ValueError("watermark cannot move backwards")
        self.watermark_ms = watermark_ms
        ready = [start for start in self._events if start + self.window_size_ms + self.allowed_lateness_ms <= watermark_ms]
        results = []
        for start in sorted(ready):
            # Python's sort is stable, so equal timestamps retain ingestion order.
            events = tuple(sorted(self._events.pop(start), key=lambda event: event.timestamp_ms))
            results.append(WindowResult(start, start + self.window_size_ms, events))
            self._finalized.add(start)
        return tuple(results)

    @property
    def late_events(self) -> tuple[Event, ...]:
        return tuple(self._late)
