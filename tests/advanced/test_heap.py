import pytest

from python.advanced.heap import MaxHeap, MinHeap


@pytest.mark.parametrize(
    ("heap_type", "expected_peek", "expected_pop_order"),
    [
        (MinHeap, -1, [-1, 2, 3, 3]),
        (MaxHeap, 3, [3, 3, 2, -1]),
    ],
)
def test_push_peek_pop_and_truthiness(heap_type, expected_peek, expected_pop_order):
    heap = heap_type()
    for value in (3, -1, 3, 2):
        heap.push(value)

    assert heap
    assert len(heap) == 4
    assert heap.peek() == expected_peek
    assert len(heap) == 4
    assert [heap.pop() for _ in range(4)] == expected_pop_order
    assert len(heap) == 0
    assert not heap


@pytest.mark.parametrize("heap_type", [MinHeap, MaxHeap])
def test_build_heap_copies_input_and_pops_in_order(heap_type):
    data = [4, -2, 7, 1, 1]
    original = list(data)
    heap = heap_type()
    heap.build_heap(data)

    assert data == original
    expected = sorted(data, reverse=heap_type is MaxHeap)
    assert [heap.pop() for _ in range(len(data))] == expected


@pytest.mark.parametrize("heap_type", [MinHeap, MaxHeap])
def test_empty_peek_and_pop_raise_index_error(heap_type):
    heap = heap_type()
    with pytest.raises(IndexError):
        heap.peek()
    with pytest.raises(IndexError):
        heap.pop()


@pytest.mark.parametrize("heap_type", [MinHeap, MaxHeap])
def test_heap_sort_is_ascending_and_does_not_mutate_input(heap_type):
    data = [5, 1, 4, 1, -3, 2]
    original = list(data)
    heap = heap_type()

    assert heap.heap_sort(data) == sorted(data)
    assert data == original


def test_min_heap_sort_drains_its_internal_heap():
    heap = MinHeap()

    assert heap.heap_sort([3, 1, 2]) == [1, 2, 3]
    assert len(heap) == 0
