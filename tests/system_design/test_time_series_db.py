import math

import pytest

from python.system_design.time_series_db import TimeSeriesDB


def test_query_sorts_out_of_order_writes_and_preserves_equal_timestamp_order():
    database = TimeSeriesDB()
    database.write("cpu", 20, 2.0)
    database.write("cpu", 10, 1.0)
    database.write("cpu", 10, 1.5)

    assert database.query("cpu", 0, 30) == [(10, 1.0), (10, 1.5), (20, 2.0)]


def test_query_bounds_are_inclusive_and_unknown_metric_does_not_mutate():
    database = TimeSeriesDB()
    database.write("cpu", 10, 1)
    database.write("cpu", 20, 2)

    assert database.query("cpu", 10, 20) == [(10, 1), (20, 2)]
    assert database.query("missing", 0, 100) == []
    assert database.data == {"cpu": [(10, 1), (20, 2)]}


def test_query_result_is_a_fresh_list():
    database = TimeSeriesDB()
    database.write("cpu", 10, 1)

    result = database.query("cpu", 0, 20)
    result.append((15, 99))

    assert database.query("cpu", 0, 20) == [(10, 1)]


@pytest.mark.parametrize("metric", ["", "   ", None, 42])
def test_write_rejects_invalid_metric(metric):
    with pytest.raises(ValueError):
        TimeSeriesDB().write(metric, 0, 1)


@pytest.mark.parametrize("timestamp", [-1, 1.5, True, None])
def test_write_rejects_invalid_timestamp(timestamp):
    with pytest.raises(ValueError):
        TimeSeriesDB().write("cpu", timestamp, 1)


@pytest.mark.parametrize("value", [math.nan, math.inf, -math.inf, True, "1"])
def test_write_rejects_invalid_value(value):
    with pytest.raises(ValueError):
        TimeSeriesDB().write("cpu", 0, value)


@pytest.mark.parametrize(
    ("start", "end"),
    [(-1, 1), (1, -1), (2, 1), (1.5, 2), (1, True)],
)
def test_query_rejects_invalid_bounds(start, end):
    database = TimeSeriesDB()
    with pytest.raises(ValueError):
        database.query("cpu", start, end)


def test_invalid_write_does_not_create_metric():
    database = TimeSeriesDB()

    with pytest.raises(ValueError):
        database.write("cpu", 0, math.nan)

    assert database.data == {}
