"""An in-memory publish/subscribe model for interview practice.

Subscriptions are keyed by (topic, subscriber_id). Re-subscribing replaces
the callback without moving the subscriber in registration order. Publishing is
best effort: callback exceptions are returned to the caller and do not prevent
later subscribers from receiving the message.

There is no persistence, replay, backpressure, concurrency control, or
delivery guarantee. This model has no print side effects.
"""

from collections import OrderedDict
from typing import Callable, Dict, List, Tuple


class PubSubSystem:
    """Broadcast messages to the current subscribers of a topic."""

    def __init__(self) -> None:
        self.topics: Dict[str, OrderedDict] = {}
        self.subscribers: Dict[str, set] = {}

    def subscribe(self, topic: str, subscriber_id: str, callback: Callable) -> None:
        self._validate_topic(topic)
        self._validate_subscriber(subscriber_id)
        if not callable(callback):
            raise ValueError("callback must be callable")

        subscriptions = self.topics.setdefault(topic, OrderedDict())
        # Existing OrderedDict keys keep their original position on assignment.
        subscriptions[subscriber_id] = callback
        self.subscribers.setdefault(subscriber_id, set()).add(topic)

    def unsubscribe(self, topic: str, subscriber_id: str) -> bool:
        """Remove a subscription; return False for an already absent one."""

        self._validate_topic(topic)
        subscriptions = self.topics.get(topic)
        if subscriptions is None or subscriber_id not in subscriptions:
            return False
        del subscriptions[subscriber_id]
        if not subscriptions:
            del self.topics[topic]
        subscriber_topics = self.subscribers.get(subscriber_id)
        if subscriber_topics is not None:
            subscriber_topics.discard(topic)
            if not subscriber_topics:
                del self.subscribers[subscriber_id]
        return True

    def publish(self, topic: str, message) -> List[Tuple[str, Exception]]:
        """Deliver in order and return (subscriber_id, exception) failures."""

        subscriptions = self.topics.get(topic)
        if not subscriptions:
            return []

        failures = []
        for subscriber_id, callback in tuple(subscriptions.items()):
            try:
                callback(subscriber_id, message)
            except Exception as error:
                failures.append((subscriber_id, error))
        return failures

    def get_subscribers(self, topic: str) -> int:
        """Return the count without creating state for an unknown topic."""

        subscriptions = self.topics.get(topic)
        return len(subscriptions) if subscriptions else 0

    @staticmethod
    def _validate_topic(topic: str) -> None:
        if not isinstance(topic, str) or not topic.strip():
            raise ValueError("topic must be a non-empty string")

    @staticmethod
    def _validate_subscriber(subscriber_id: str) -> None:
        if not isinstance(subscriber_id, str) or not subscriber_id.strip():
            raise ValueError("subscriber_id must be a non-empty string")


class Subscriber:
    """Convenience callback object for the module example."""

    def __init__(self, name: str) -> None:
        self.name = name

    def on_message(self, subscriber_id: str, message) -> None:
        return None


if __name__ == "__main__":
    pubsub = PubSubSystem()
    received = []
    pubsub.subscribe("news", "reader", lambda sid, message: received.append(message))
    pubsub.publish("news", "hello")
    print(received)
