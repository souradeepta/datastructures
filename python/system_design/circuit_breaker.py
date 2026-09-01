"""A synchronous circuit breaker teaching model.

The breaker counts consecutive operation failures. It transitions from CLOSED
to OPEN at the configured threshold, permits one clock-driven probe in
HALF_OPEN, and closes after a successful probe. Service errors are always
re-raised.

This model does not provide concurrency coordination, sliding windows,
distributed state, or operation timeout enforcement.
"""

from enum import Enum
import time
from typing import Callable, Optional


class State(Enum):
    CLOSED = "closed"
    OPEN = "open"
    HALF_OPEN = "half_open"


CircuitState = State


class CircuitOpenError(RuntimeError):
    """Raised when the circuit is open or a half-open probe is in progress."""


class CircuitBreaker:
    """Protect calls to one dependency using consecutive-failure detection."""

    def __init__(
        self,
        failure_threshold: int = 5,
        reset_timeout: float = 30.0,
        clock: Optional[Callable[[], float]] = None,
    ) -> None:
        if isinstance(failure_threshold, bool) or not isinstance(failure_threshold, int):
            raise ValueError("failure_threshold must be a positive integer")
        if failure_threshold <= 0:
            raise ValueError("failure_threshold must be a positive integer")
        if isinstance(reset_timeout, bool) or not isinstance(reset_timeout, (int, float)):
            raise ValueError("reset_timeout must be non-negative")
        if reset_timeout < 0:
            raise ValueError("reset_timeout must be non-negative")
        if clock is not None and not callable(clock):
            raise ValueError("clock must be callable")

        self.failure_threshold = failure_threshold
        self.reset_timeout = float(reset_timeout)
        self.clock = clock or time.monotonic
        self.state = State.CLOSED
        self.failures = 0
        self._opened_at = None
        self._probe_in_flight = False

    @property
    def threshold(self) -> int:
        return self.failure_threshold

    def call(self, operation: Callable):
        """Execute operation or fail fast while the circuit is open."""

        if not callable(operation):
            raise ValueError("operation must be callable")

        probe = False
        if self.state is State.OPEN:
            if self.clock() - self._opened_at < self.reset_timeout:
                raise CircuitOpenError("circuit is open")
            self.state = State.HALF_OPEN

        if self.state is State.HALF_OPEN:
            if self._probe_in_flight:
                raise CircuitOpenError("half-open probe is in progress")
            self._probe_in_flight = True
            probe = True

        try:
            result = operation()
        except Exception:
            if probe:
                self._probe_in_flight = False
                self._open()
            else:
                self.failures += 1
                if self.failures >= self.failure_threshold:
                    self._open()
            raise
        else:
            self._probe_in_flight = False
            self.failures = 0
            self.state = State.CLOSED
            self._opened_at = None
            return result

    def _open(self) -> None:
        self.state = State.OPEN
        self._opened_at = self.clock()


if __name__ == "__main__":
    breaker = CircuitBreaker(failure_threshold=2)
    for _ in range(2):
        try:
            breaker.call(lambda: (_ for _ in ()).throw(RuntimeError("down")))
        except RuntimeError:
            pass
    print(breaker.state)
