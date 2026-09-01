"""A sorted, in-memory time-series model for interview practice.

``TimeSeriesDB`` accepts timestamped finite numeric samples, supports writes in
any order, and keeps equal timestamps in their original write order. It does
not provide persistence, concurrency control, retention automation,
aggregation, downsampling, authentication, or production capacity claims.
"""

from __future__ import annotations

from math import isfinite
from numbers import Real


class TimeSeriesDB:
    """Store and query timestamped samples without mutating on reads."""

    def __init__(self) -> None:
        self.data: dict[str, list[tuple[int, Real]]] = {}

    @staticmethod
    def _validate_metric(metric: object) -> None:
        if not isinstance(metric, str) or not metric.strip():
            raise ValueError("metric must be a non-empty string")

    @staticmethod
    def _validate_timestamp(timestamp_ms: object, name: str = "timestamp_ms") -> None:
        if (
            isinstance(timestamp_ms, bool)
            or not isinstance(timestamp_ms, int)
            or timestamp_ms < 0
        ):
            raise ValueError(f"{name} must be a non-negative integer")

    @staticmethod
    def _validate_value(value: object) -> None:
        if (
            isinstance(value, bool)
            or not isinstance(value, Real)
            or not isfinite(float(value))
        ):
            raise ValueError("value must be a finite number")

    def write(self, metric: str, timestamp_ms: int, value: Real) -> None:
        """Append a validated sample, preserving write order for ties."""
        self._validate_metric(metric)
        self._validate_timestamp(timestamp_ms)
        self._validate_value(value)
        self.data.setdefault(metric, []).append((timestamp_ms, value))

    def query(self, metric: str, start_ms: int, end_ms: int) -> list[tuple[int, Real]]:
        """Return inclusive samples in timestamp order.

        Unknown metrics return an empty list without creating a metric key.
        """
        self._validate_metric(metric)
        self._validate_timestamp(start_ms, "start_ms")
        self._validate_timestamp(end_ms, "end_ms")
        if start_ms > end_ms:
            raise ValueError("start_ms must not exceed end_ms")
        samples = self.data.get(metric)
        if samples is None:
            return []
        return sorted(
            (
                (timestamp, value)
                for timestamp, value in samples
                if start_ms <= timestamp <= end_ms
            ),
            key=lambda sample: sample[0],
        )


if __name__ == "__main__":
    database = TimeSeriesDB()
    database.write("cpu", 1000, 50)
    print(database.query("cpu", 0, 2000))
