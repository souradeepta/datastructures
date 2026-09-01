import math

import pytest

from python.advanced.segment_tree import RangeMaxTree, RangeMinTree, SegmentTree


def test_sum_queries_updates_and_input_non_mutation():
    data = [1, 3, 5, 7, 9]
    original = list(data)
    tree = SegmentTree(data)

    assert tree.query(0, 4) == 25
    assert tree.query(1, 3) == 15
    tree.update(2, 10)
    assert tree.query(0, 4) == 30
    assert data == original


def test_min_max_and_custom_aggregation():
    data = [12, 18, 6, 9, 15]
    assert RangeMinTree(data).query(1, 4) == 6
    assert RangeMaxTree(data).query(1, 4) == 18

    gcd_tree = SegmentTree(data, func=math.gcd, identity=0)
    assert gcd_tree.query(0, 4) == 3
    gcd_tree.update(2, 21)
    assert gcd_tree.query(1, 3) == 3


def test_empty_and_invalid_ranges_and_indexes():
    empty = SegmentTree([])
    with pytest.raises(IndexError):
        empty.query(0, 0)
    with pytest.raises(IndexError):
        empty.update(0, 1)

    tree = SegmentTree([1, 2, 3])
    for operation in (
        lambda: tree.query(-1, 1),
        lambda: tree.query(0, 3),
        lambda: tree.query(2, 1),
        lambda: tree.update(-1, 0),
        lambda: tree.update(3, 0),
    ):
        with pytest.raises(IndexError):
            operation()
