import pytest

from python.advanced.fenwick_tree import FenwickTree, count_inversions


def test_build_queries_updates_and_point_values():
    tree = FenwickTree.build([2, -1, 4, 3])

    assert tree.prefix_sum(0) == 2
    assert tree.prefix_sum(3) == 8
    assert tree.range_query(1, 2) == 3
    assert tree.point_value(1) == -1

    tree.update(1, 5)
    assert tree.point_value(1) == 4
    assert tree.range_query(0, 3) == 13


def test_invalid_sizes_indexes_and_ranges_fail_fast():
    with pytest.raises(ValueError):
        FenwickTree(-1)

    tree = FenwickTree(3)
    for operation in (
        lambda: tree.update(-1, 1),
        lambda: tree.update(3, 1),
        lambda: tree.prefix_sum(-1),
        lambda: tree.prefix_sum(3),
        lambda: tree.point_value(-1),
        lambda: tree.range_query(-1, 1),
        lambda: tree.range_query(0, 3),
    ):
        with pytest.raises(IndexError):
            operation()

    with pytest.raises(ValueError):
        tree.range_query(2, 1)

    with pytest.raises(IndexError):
        FenwickTree(0).prefix_sum(0)


def test_count_inversions_handles_negative_sparse_and_duplicate_values():
    assert count_inversions([]) == 0
    assert count_inversions([-10, 5, -10, -20]) == 4
    assert count_inversions([3, 1, 2, 1]) == 4
    assert count_inversions([1, 2, 3]) == 0
    assert count_inversions([3, 2, 1]) == 3
