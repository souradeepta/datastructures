"""Deterministic canary rollout and guardrail teaching model."""

from __future__ import annotations

import hashlib


class ModelRollout:
    """Assign users to baseline/candidate and gate promotion on safety metrics."""

    def __init__(
        self,
        baseline_version: str,
        candidate_version: str,
        candidate_percentage: int = 0,
        min_quality: float = 0.0,
        max_latency_ms: float = float("inf"),
        max_error_rate: float = 1.0,
        salt: str = "interviewprep",
    ) -> None:
        if not baseline_version or not candidate_version or baseline_version == candidate_version:
            raise ValueError("versions must be non-empty and different")
        if not 0 <= candidate_percentage <= 100:
            raise ValueError("candidate_percentage must be between 0 and 100")
        if min_quality < 0 or max_latency_ms <= 0 or not 0 <= max_error_rate <= 1:
            raise ValueError("invalid rollout guardrails")
        self.baseline_version = baseline_version
        self.candidate_version = candidate_version
        self.candidate_percentage = candidate_percentage
        self.min_quality = min_quality
        self.max_latency_ms = max_latency_ms
        self.max_error_rate = max_error_rate
        self.salt = salt
        self._latencies: list[float] = []
        self._errors = 0
        self._previous_baseline: str | None = None

    def version_for(self, user_id: str) -> str:
        if not isinstance(user_id, str) or not user_id:
            raise ValueError("user_id must be a non-empty string")
        bucket = int.from_bytes(hashlib.sha256(f"{self.salt}:{user_id}".encode()).digest()[:8], "big") % 100
        return self.candidate_version if bucket < self.candidate_percentage else self.baseline_version

    assign = version_for

    def serve(self, user_id: str, predict):
        """Call ``predict`` with the selected version and propagate its errors."""
        if not callable(predict):
            raise TypeError("predict must be callable")
        return predict(self.version_for(user_id))

    def set_candidate_percentage(self, percentage: int) -> None:
        if not isinstance(percentage, int) or isinstance(percentage, bool) or not 0 <= percentage <= 100:
            raise ValueError("candidate_percentage must be an integer from 0 to 100")
        self.candidate_percentage = percentage

    def record_observation(self, latency_ms: float, error: bool = False) -> None:
        if latency_ms < 0:
            raise ValueError("latency_ms must be non-negative")
        self._latencies.append(float(latency_ms))
        if error:
            self._errors += 1

    @property
    def error_rate(self) -> float:
        return self._errors / len(self._latencies) if self._latencies else 0.0

    @property
    def average_latency_ms(self) -> float:
        return sum(self._latencies) / len(self._latencies) if self._latencies else 0.0

    def promote(self, offline_quality: float) -> None:
        if offline_quality < self.min_quality:
            raise RuntimeError("offline quality gate failed")
        if self.average_latency_ms > self.max_latency_ms or self.error_rate > self.max_error_rate:
            raise RuntimeError("online guardrail failed")
        self._previous_baseline = self.baseline_version
        self.baseline_version = self.candidate_version
        self.candidate_percentage = 0

    def rollback(self) -> None:
        if self._previous_baseline is not None:
            self.baseline_version, self.candidate_version = (
                self._previous_baseline,
                self.baseline_version,
            )
            self._previous_baseline = None
        self.candidate_percentage = 0
