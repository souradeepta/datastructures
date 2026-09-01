import pytest

from python.system_design.circuit_breaker import (
    CircuitBreaker,
    CircuitOpenError,
    State,
)


class FakeClock:
    def __init__(self):
        self.now = 0.0

    def __call__(self):
        return self.now


def test_failures_open_circuit_and_open_calls_fail_fast():
    clock = FakeClock()
    breaker = CircuitBreaker(failure_threshold=2, reset_timeout=5, clock=clock)

    with pytest.raises(RuntimeError):
        breaker.call(lambda: (_ for _ in ()).throw(RuntimeError("down")))
    assert breaker.state is State.CLOSED
    with pytest.raises(RuntimeError):
        breaker.call(lambda: (_ for _ in ()).throw(RuntimeError("down")))
    assert breaker.state is State.OPEN

    with pytest.raises(CircuitOpenError):
        breaker.call(lambda: "not called")


def test_clock_drives_single_probe_and_success_closes_and_resets_failures():
    clock = FakeClock()
    breaker = CircuitBreaker(failure_threshold=1, reset_timeout=5, clock=clock)

    with pytest.raises(RuntimeError):
        breaker.call(lambda: (_ for _ in ()).throw(RuntimeError("down")))
    clock.now = 5
    assert breaker.call(lambda: "healthy") == "healthy"
    assert breaker.state is State.CLOSED
    assert breaker.failures == 0


def test_failed_half_open_probe_reopens_the_circuit():
    clock = FakeClock()
    breaker = CircuitBreaker(failure_threshold=1, reset_timeout=5, clock=clock)

    with pytest.raises(RuntimeError):
        breaker.call(lambda: (_ for _ in ()).throw(RuntimeError("down")))
    clock.now = 5
    with pytest.raises(RuntimeError):
        breaker.call(lambda: (_ for _ in ()).throw(RuntimeError("still down")))
    assert breaker.state is State.OPEN
    with pytest.raises(CircuitOpenError):
        breaker.call(lambda: "not called")


@pytest.mark.parametrize(
    "kwargs",
    [
        {"failure_threshold": 0},
        {"failure_threshold": True},
        {"reset_timeout": -1},
        {"reset_timeout": True},
        {"clock": 42},
    ],
)
def test_configuration_is_validated(kwargs):
    with pytest.raises(ValueError):
        CircuitBreaker(**kwargs)


def test_service_errors_are_propagated():
    breaker = CircuitBreaker()
    error = ValueError("service error")
    with pytest.raises(ValueError, match="service error"):
        breaker.call(lambda: (_ for _ in ()).throw(error))
