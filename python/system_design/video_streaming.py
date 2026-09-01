"""A small, synchronous video-streaming model for interview practice.

``Stream`` stores videos and fixed renditions in memory. Uploading performs a
fake synchronous transcode so every accepted video is immediately ready. The
model deliberately omits persistence, concurrency, authentication, retries,
CDN delivery, adaptive segmentation, and production capacity guarantees.
"""

from __future__ import annotations

from dataclasses import dataclass
from math import isfinite
from numbers import Real
from types import MappingProxyType
from typing import Mapping, Optional


QUALITY_BITRATES: Mapping[str, float] = MappingProxyType(
    {"480p": 1.5, "720p": 3.0, "1080p": 6.0}
)


@dataclass(frozen=True)
class Video:
    """An immutable, ready video and its fixed bitrate ladder."""

    video_id: str
    title: str
    renditions: Mapping[str, float]
    ready: bool = True

    def __post_init__(self) -> None:
        object.__setattr__(self, "renditions", MappingProxyType(dict(self.renditions)))

    @property
    def uid(self) -> str:
        """Compatibility alias for the identifier used by older examples."""
        return self.video_id

    @property
    def name(self) -> str:
        """Compatibility alias for the title used by older examples."""
        return self.title

    @property
    def bitrates(self) -> tuple[str, ...]:
        """Return rendition names without exposing mutable internal state."""
        return tuple(self.renditions)


class Transcoder:
    """Create the fixed rendition ladder used by this teaching model."""

    def transcode(self, video: Video) -> Video:
        return Video(video.video_id, video.title, QUALITY_BITRATES)


class Stream:
    """In-memory video catalog with deterministic quality selection."""

    def __init__(self, transcoder: Optional[Transcoder] = None) -> None:
        self._videos: dict[str, Video] = {}
        self.transcoder = transcoder or Transcoder()

    @property
    def videos(self) -> dict[str, Video]:
        """Return a catalog copy; individual videos are immutable."""
        return dict(self._videos)

    def upload(self, video_id: str, title: str) -> Video:
        """Store and synchronously transcode a new video.

        Empty or whitespace-only strings raise ``ValueError``. Duplicate IDs
        are rejected before the catalog changes.
        """
        if not isinstance(video_id, str) or not video_id.strip():
            raise ValueError("video_id must be a non-empty string")
        if not isinstance(title, str) or not title.strip():
            raise ValueError("title must be a non-empty string")
        if video_id in self._videos:
            raise ValueError(f"video already exists: {video_id}")
        video = self.transcoder.transcode(Video(video_id, title, {}))
        self._videos[video_id] = video
        return video

    def select_quality(self, video_id: str, bandwidth_mbps: Real) -> Optional[str]:
        """Return the highest rendition sustainable by available bandwidth.

        The bandwidth is measured in Mbps. Values below 1.5 return ``None``;
        unknown videos raise ``KeyError`` and invalid bandwidth raises
        ``ValueError``.
        """
        if video_id not in self._videos:
            raise KeyError(video_id)
        if (
            isinstance(bandwidth_mbps, bool)
            or not isinstance(bandwidth_mbps, Real)
            or not isfinite(float(bandwidth_mbps))
            or bandwidth_mbps < 0
        ):
            raise ValueError("bandwidth_mbps must be a finite non-negative number")
        choices = [
            quality
            for quality, bitrate in self._videos[video_id].renditions.items()
            if bitrate <= bandwidth_mbps
        ]
        return choices[-1] if choices else None

    def get_video(self, video_id: str) -> Video:
        """Return an immutable video record or raise ``KeyError``."""
        return self._videos[video_id]


if __name__ == "__main__":
    stream = Stream()
    stream.upload("demo", "A short film")
    print(stream.select_quality("demo", 5))
