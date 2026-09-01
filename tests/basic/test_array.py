import pytest

from python.basic.array import DynamicArray


def test_append_resize_and_iteration():
    array = DynamicArray()
    for value in range(5):
        array.append(value)

    assert list(array) == [0, 1, 2, 3, 4]
    assert len(array) == 5
    assert array.capacity() == 8


def test_insert_delete_and_index_access():
    array = DynamicArray()
    for value in (1, 3, 4):
        array.append(value)

    array.insert(1, 2)
    array.insert(4, 5)
    assert list(array) == [1, 2, 3, 4, 5]
    assert array[2] == 3

    assert array.delete(1) == 2
    array[1] = 20
    assert list(array) == [1, 20, 4, 5]


def test_resize_shrinks_but_keeps_default_capacity():
    array = DynamicArray()
    for value in range(16):
        array.append(value)
    assert array.capacity() == 16

    for _ in range(12):
        array.delete(0)
    assert list(array) == [12, 13, 14, 15]
    assert array.capacity() == 8

    for _ in range(3):
        array.delete(0)
    assert array.capacity() == 4


def test_invalid_indices_raise_index_error():
    array = DynamicArray()
    with pytest.raises(IndexError):
        array.get(0)
    with pytest.raises(IndexError):
        array.set(0, "value")
    with pytest.raises(IndexError):
        array.delete(0)
    with pytest.raises(IndexError):
        array.insert(1, "value")
