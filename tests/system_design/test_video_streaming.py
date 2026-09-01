import math

import pytest

from python.system_design.video_streaming import Stream


def test_upload_is_ready_with_fixed_rendition_ladder():
    stream = Stream()

    video = stream.upload("intro", "Interview Prep")

    assert video.video_id == "intro"
    assert video.title == "Interview Prep"
    assert video.ready
    assert dict(video.renditions) == {"480p": 1.5, "720p": 3.0, "1080p": 6.0}
    assert video.bitrates == ("480p", "720p", "1080p")


@pytest.mark.parametrize(
    ("bandwidth", "expected"),
    [
        (0, None),
        (1.49, None),
        (1.5, "480p"),
        (2.99, "480p"),
        (3, "720p"),
        (5.99, "720p"),
        (6, "1080p"),
        (100, "1080p"),
    ],
)
def test_select_quality_uses_inclusive_bitrate_boundaries(bandwidth, expected):
    stream = Stream()
    stream.upload("intro", "Interview Prep")

    assert stream.select_quality("intro", bandwidth) == expected


@pytest.mark.parametrize("video_id", ["", "   ", 42, None])
def test_upload_rejects_invalid_video_id(video_id):
    with pytest.raises(ValueError):
        Stream().upload(video_id, "Title")


@pytest.mark.parametrize("title", ["", "   ", 42, None])
def test_upload_rejects_invalid_title(title):
    with pytest.raises(ValueError):
        Stream().upload("intro", title)


def test_duplicate_and_unknown_video_errors_do_not_change_catalog():
    stream = Stream()
    stream.upload("intro", "Interview Prep")

    with pytest.raises(ValueError):
        stream.upload("intro", "Another title")
    with pytest.raises(KeyError):
        stream.select_quality("missing", 3)

    assert list(stream.videos) == ["intro"]


@pytest.mark.parametrize("bandwidth", [-1, math.nan, math.inf, -math.inf, "3", True])
def test_select_quality_rejects_invalid_bandwidth(bandwidth):
    stream = Stream()
    stream.upload("intro", "Interview Prep")

    with pytest.raises(ValueError):
        stream.select_quality("intro", bandwidth)


def test_returned_video_and_catalog_state_are_isolated():
    stream = Stream()
    video = stream.upload("intro", "Interview Prep")
    catalog = stream.videos
    catalog.clear()

    assert stream.get_video("intro") == video
    assert stream.select_quality("intro", 6) == "1080p"
    with pytest.raises(TypeError):
        video.renditions["1440p"] = 10
