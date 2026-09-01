import pytest
from python.basic.queue_ds import CircularQueue, Queue


class TestQueue:
    def test_enqueue_dequeue(self):
        q = Queue()
        q.enqueue(1)
        q.enqueue(2)
        assert q.dequeue() == 1
        assert q.dequeue() == 2

    def test_peek(self):
        q = Queue()
        q.enqueue(10)
        assert q.peek() == 10
        assert q.size() == 1

    def test_is_empty(self):
        q = Queue()
        assert q.is_empty()
        q.enqueue(1)
        assert not q.is_empty()

    def test_dequeue_empty_raises(self):
        q = Queue()
        with pytest.raises(IndexError):
            q.dequeue()

    def test_fifo_order(self):
        q = Queue()
        for i in range(5):
            q.enqueue(i)
        result = [q.dequeue() for _ in range(5)]
        assert result == [0, 1, 2, 3, 4]

    def test_circular_queue_fixed_capacity_overflow(self):
        q = CircularQueue(2)
        q.enqueue(1)
        q.enqueue(2)
        with pytest.raises(OverflowError):
            q.enqueue(3)
        assert q.dequeue() == 1
        q.enqueue(3)
        assert q.dequeue() == 2
        assert q.dequeue() == 3
