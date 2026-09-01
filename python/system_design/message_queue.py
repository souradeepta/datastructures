"""A small in-memory message queue for interview practice.

The model has explicitly created topics, FIFO ready queues, immutable message
records, and an in-flight set. A message is removed permanently by ack or
returned to the ready queue by nack(..., requeue=True).

This is deliberately not a broker: it has no persistence, consumer groups,
partitions, visibility timeouts, concurrency control, or crash recovery.
"""

from collections import deque
from dataclasses import dataclass
from typing import Any, Deque, Dict, Union


@dataclass(frozen=True)
class Message:
    """An immutable message envelope assigned by one MessageQueue."""

    id: int
    topic: str
    payload: Any

    @property
    def message_id(self) -> int:
        """Readable alias for callers that use broker terminology."""

        return self.id


class Topic:
    """Internal FIFO state for one explicitly created topic."""

    def __init__(self, name: str) -> None:
        self.name = name
        self.queue: Deque[Message] = deque()
        self.in_flight: Dict[int, Message] = {}


class MessageQueue:
    """An in-memory FIFO queue with explicit acknowledgement semantics."""

    def __init__(self) -> None:
        self.topics: Dict[str, Topic] = {}
        self._next_id = 1

    def create_topic(self, topic: str) -> None:
        """Create topic; duplicate creation is rejected."""

        self._validate_topic(topic)
        if topic in self.topics:
            raise ValueError("topic already exists: %s" % topic)
        self.topics[topic] = Topic(topic)

    def publish(self, topic: str, payload: Any) -> Message:
        """Append a message and return its immutable envelope."""

        state = self._topic(topic)
        message = Message(self._next_id, topic, payload)
        self._next_id += 1
        state.queue.append(message)
        return message

    def consume(self, topic: str, limit: int = 1) -> list:
        """Move up to limit ready messages into the in-flight set."""

        state = self._topic(topic)
        if isinstance(limit, bool) or not isinstance(limit, int) or limit <= 0:
            raise ValueError("limit must be a positive integer")

        delivered = []
        for _ in range(min(limit, len(state.queue))):
            message = state.queue.popleft()
            state.in_flight[message.id] = message
            delivered.append(message)
        return delivered

    def ack(self, message: Union[Message, int]) -> bool:
        """Acknowledge an in-flight message and remove it permanently."""

        state, message_id = self._find_in_flight(message)
        del state.in_flight[message_id]
        return True

    def nack(self, message: Union[Message, int], requeue: bool = True) -> bool:
        """Reject an in-flight message, optionally returning it to the FIFO."""

        if not isinstance(requeue, bool):
            raise ValueError("requeue must be a boolean")
        state, message_id = self._find_in_flight(message)
        rejected = state.in_flight.pop(message_id)
        if requeue:
            state.queue.appendleft(rejected)
        return True

    def pending_count(self, topic: str) -> int:
        return len(self._topic(topic).queue)

    def in_flight_count(self, topic: str) -> int:
        return len(self._topic(topic).in_flight)

    @staticmethod
    def _validate_topic(topic: str) -> None:
        if not isinstance(topic, str) or not topic.strip():
            raise ValueError("topic must be a non-empty string")

    def _topic(self, topic: str) -> Topic:
        self._validate_topic(topic)
        try:
            return self.topics[topic]
        except KeyError:
            raise KeyError("unknown topic: %s" % topic)

    def _find_in_flight(self, message: Union[Message, int]):
        message_id = message.id if isinstance(message, Message) else message
        if not isinstance(message_id, int) or isinstance(message_id, bool):
            raise KeyError("message is not in flight: %r" % (message,))
        for state in self.topics.values():
            if message_id in state.in_flight:
                return state, message_id
        raise KeyError("message is not in flight: %r" % (message_id,))


if __name__ == "__main__":
    queue = MessageQueue()
    queue.create_topic("events")
    queue.publish("events", "hello")
    message = queue.consume("events")[0]
    queue.ack(message)
    print("acknowledged", message.id)
