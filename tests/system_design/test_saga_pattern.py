from python.system_design.saga_pattern import SagaOrchestrator, SagaStep


def test_success_executes_actions_in_order_and_reports_completion():
    events = []
    saga = SagaOrchestrator()
    saga.add_step(SagaStep("reserve", lambda: events.append("reserve"), lambda: events.append("undo reserve")))
    saga.add_step(SagaStep("charge", lambda: events.append("charge"), lambda: events.append("undo charge")))

    result = saga.execute()

    assert result.success
    assert result.failed_step is None
    assert result.completed_steps == ["reserve", "charge"]
    assert result.compensation_failures == []
    assert events == ["reserve", "charge"]


def test_failure_stops_and_compensates_completed_steps_in_reverse_order():
    events = []

    def fail():
        events.append("charge")
        raise RuntimeError("card declined")

    saga = SagaOrchestrator()
    saga.add_step(SagaStep("reserve", lambda: events.append("reserve"), lambda: events.append("release")))
    saga.add_step(SagaStep("charge", fail, lambda: events.append("undo charge")))
    saga.add_step(SagaStep("notify", lambda: events.append("notify"), lambda: events.append("undo notify")))

    result = saga.execute()

    assert not result.success
    assert result.failed_step == "charge"
    assert result.completed_steps == ["reserve"]
    assert result.compensation_failures == []
    assert events == ["reserve", "charge", "release"]


def test_compensation_failures_are_reported_and_execution_is_reusable():
    events = []
    should_fail = [True]

    def action():
        events.append("action")

    def compensation():
        events.append("compensate")
        if should_fail[0]:
            raise RuntimeError("cleanup unavailable")

    saga = SagaOrchestrator()
    saga.add_step(SagaStep("first", action, compensation))
    saga.add_step(SagaStep("second", lambda: (_ for _ in ()).throw(RuntimeError("stop")), lambda: None))

    first = saga.execute()
    assert first.compensation_failures == ["first"]
    assert saga.executed == ["first"]

    should_fail[0] = False
    second = saga.execute()
    assert second.compensation_failures == []
    assert second.completed_steps == ["first"]
    assert saga.executed == ["first"]
