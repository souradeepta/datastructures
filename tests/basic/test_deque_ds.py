import pytest

from python.basic.deque_ds import ArrayDeque, LinkedDeque


@pytest.mark.parametrize("deque_type", [ArrayDeque, LinkedDeque])
def test_both_deques_preserve_front_to_back_order(deque_type):
    deque = deque_type()
    deque.push_back(2)
    deque.push_front(1)
    deque.push_back(3)

    assert deque.peek_front() == 1
    assert deque.peek_back() == 3
    assert deque.size() == 3
    assert [deque.pop_front(), deque.pop_back(), deque.pop_front()] == [1, 3, 2]
    assert deque.is_empty()


def test_array_deque_wraparound_and_resize():
    deque = ArrayDeque()
    for value in range(8):
        deque.push_back(value)
    for value in range(3):
        assert deque.pop_front() == value
    for value in range(8, 13):
        deque.push_back(value)

    assert deque._capacity >= 16
    assert [deque.pop_front() for _ in range(10)] == list(range(3, 13))


@pytest.mark.parametrize("deque_type", [ArrayDeque, LinkedDeque])
def test_empty_operations_raise_index_error(deque_type):
    deque = deque_type()
    for operation in (deque.pop_front, deque.pop_back, deque.peek_front, deque.peek_back):
        with pytest.raises(IndexError):
            operation()
