import pytest

from python.distributed_systems.event_time_windows import EventTimeWindows


def test_out_of_order_events_are_sorted_and_windows_are_half_open():
    windows = EventTimeWindows(window_size_ms=10)
    assert windows.add_event("two", 12, 2) == "accepted"
    assert windows.add_event("one", 3, 1) == "accepted"
    assert windows.add_event("boundary", 10, 10) == "accepted"
    results = windows.advance_watermark(20)
    assert [(result.start_ms, result.end_ms) for result in results] == [(0, 10), (10, 20)]
    assert [event.event_id for event in results[0].events] == ["one"]
    assert [event.event_id for event in results[1].events] == ["boundary", "two"]


def test_duplicates_and_late_events_are_side_outputs():
    windows = EventTimeWindows(10, allowed_lateness_ms=2)
    assert windows.add_event("one", 5, 1) == "accepted"
    assert windows.add_event("one", 5, 99) == "duplicate"
    assert windows.advance_watermark(11) == ()
    assert windows.advance_watermark(11) == ()
    assert windows.advance_watermark(12)[0].total == 1
    assert windows.add_event("late", 5, 2) == "late"
    assert [event.event_id for event in windows.late_events] == ["late"]


def test_watermark_and_configuration_validation():
    with pytest.raises(ValueError):
        EventTimeWindows(0)
    windows = EventTimeWindows(10)
    windows.advance_watermark(10)
    with pytest.raises(ValueError):
        windows.advance_watermark(9)
    with pytest.raises(ValueError):
        windows.add_event("bad", -1, 1)
