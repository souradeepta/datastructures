import dataclasses

import pytest

from python.system_design.message_queue import Message, MessageQueue


def test_publish_assigns_immutable_monotonic_messages_and_consumes_fifo():
    queue = MessageQueue()
    queue.create_topic("jobs")

    first = queue.publish("jobs", {"job": 1})
    second = queue.publish("jobs", {"job": 2})

    assert isinstance(first, Message)
    assert [message.id for message in queue.consume("jobs", limit=2)] == [1, 2]
    assert first.message_id < second.message_id
    assert queue.in_flight_count("jobs") == 2
    with pytest.raises(dataclasses.FrozenInstanceError):
        first.id = 99


def test_consume_batches_without_duplicate_delivery_and_ack_removes_messages():
    queue = MessageQueue()
    queue.create_topic("jobs")
    messages = [queue.publish("jobs", index) for index in range(3)]

    assert queue.consume("jobs", 2) == messages[:2]
    assert queue.consume("jobs", 2) == [messages[2]]
    assert queue.consume("jobs", 2) == []
    assert queue.in_flight_count("jobs") == 3

    assert queue.ack(messages[0])
    assert queue.in_flight_count("jobs") == 2
    with pytest.raises(KeyError):
        queue.ack(messages[0])


def test_nack_requeues_at_front_or_discards():
    queue = MessageQueue()
    queue.create_topic("jobs")
    first = queue.publish("jobs", "first")
    second = queue.publish("jobs", "second")

    delivered = queue.consume("jobs", 1)
    queue.nack(delivered[0])
    assert queue.consume("jobs", 2) == [first, second]

    queue.nack(second, requeue=False)
    assert queue.consume("jobs") == []


def test_topics_must_be_created_explicitly_and_validate_limits():
    queue = MessageQueue()
    with pytest.raises(KeyError):
        queue.publish("missing", "payload")
    with pytest.raises(KeyError):
        queue.consume("missing")
    queue.create_topic("jobs")
    with pytest.raises(ValueError):
        queue.create_topic("jobs")
    for limit in [0, -1, True, "2"]:
        with pytest.raises(ValueError):
            queue.consume("jobs", limit)
