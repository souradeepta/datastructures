import pytest

from python.system_design.pub_sub_system import PubSubSystem


def test_subscribe_is_idempotent_and_replacement_preserves_order():
    system = PubSubSystem()
    calls = []
    system.subscribe("news", "a", lambda sid, message: calls.append(("old", sid, message)))
    system.subscribe("news", "b", lambda sid, message: calls.append(("b", sid, message)))
    system.subscribe("news", "a", lambda sid, message: calls.append(("new", sid, message)))

    assert system.get_subscribers("news") == 2
    assert system.publish("news", "hello") == []
    assert calls == [("new", "a", "hello"), ("b", "b", "hello")]


def test_publish_collects_failures_and_continues_in_registration_order():
    system = PubSubSystem()
    calls = []

    def failing(sid, message):
        calls.append(sid)
        raise RuntimeError("subscriber unavailable")

    system.subscribe("events", "bad", failing)
    system.subscribe("events", "good", lambda sid, message: calls.append(sid))

    failures = system.publish("events", 42)

    assert calls == ["bad", "good"]
    assert len(failures) == 1
    assert failures[0][0] == "bad"
    assert isinstance(failures[0][1], RuntimeError)


def test_unsubscribe_is_safe_and_unknown_reads_do_not_create_state():
    system = PubSubSystem()
    assert system.get_subscribers("missing") == 0
    assert system.topics == {}
    assert system.unsubscribe("missing", "reader") is False
    assert system.topics == {}

    received = []
    system.subscribe("news", "reader", lambda sid, message: received.append(message))
    assert system.unsubscribe("news", "reader") is True
    assert system.unsubscribe("news", "reader") is False
    assert system.publish("news", "ignored") == []
    assert received == []
    assert system.topics == {}


@pytest.mark.parametrize(
    "args",
    [
        ("", "reader", lambda sid, message: None),
        ("news", "", lambda sid, message: None),
        ("news", "reader", None),
    ],
)
def test_subscriptions_validate_inputs(args):
    with pytest.raises(ValueError):
        PubSubSystem().subscribe(*args)
