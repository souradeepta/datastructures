"""A small fan-out-on-write news-feed model for interview practice.

Posts are immutable records with process-local monotonically increasing IDs.
Each post is copied into the author's feed and the feeds of followers who
already followed that author. This is intentionally an in-memory teaching
model: it has no persistence, concurrency control, authentication,
authorization, retries, ranking, deletion, backfill, unfollow, or distributed
fan-out.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Hashable


@dataclass(frozen=True)
class Post:
    """An immutable feed item."""

    id: int
    author: Hashable
    content: str

    @property
    def post_id(self) -> int:
        """Readable alias for callers that prefer an explicit ID name."""
        return self.id


class NewsFeeder:
    """A deterministic, process-local fan-out-on-write feed."""

    def __init__(self) -> None:
        self._followers: dict[Hashable, set[Hashable]] = {}
        self._feeds: dict[Hashable, list[Post]] = {}
        self._posts: dict[int, Post] = {}
        self._next_post_id = 1

    @property
    def posts(self) -> dict[int, Post]:
        """Return a catalog copy; the immutable posts remain stored safely."""
        return dict(self._posts)

    @property
    def followers(self) -> dict[Hashable, set[Hashable]]:
        """Return a copy of the follow graph."""
        return {author: set(followers) for author, followers in self._followers.items()}

    @property
    def feeds(self) -> dict[Hashable, list[Post]]:
        """Return copied feed lists so callers cannot alter stored feeds."""
        return {user: list(feed) for user, feed in self._feeds.items()}

    def follow(self, follower: Hashable, author: Hashable) -> None:
        """Make *follower* receive future posts by *author*.

        Following is idempotent. Self-following is rejected because the author
        already receives their own posts.
        """
        if follower == author:
            raise ValueError("a user cannot follow themself")
        self._followers.setdefault(author, set()).add(follower)

    def post(self, author: Hashable, content: str) -> Post:
        """Create a post and fan it out to the author and current followers."""
        if not isinstance(content, str):
            raise TypeError("post content must be a string")
        post = Post(self._next_post_id, author, content)
        self._next_post_id += 1
        self._posts[post.id] = post
        recipients = {author} | self._followers.get(author, set())
        for recipient in recipients:
            self._feeds.setdefault(recipient, []).insert(0, post)
        return post

    def get_feed(self, user: Hashable, limit: int = 10) -> list[Post]:
        """Return a fresh reverse-chronological feed limited to *limit* items."""
        if isinstance(limit, bool) or not isinstance(limit, int) or limit < 0:
            raise ValueError("limit must be a non-negative integer")
        return list(self._feeds.get(user, ())[:limit])


if __name__ == "__main__":
    feed = NewsFeeder()
    feed.follow("alice", "bob")
    feed.post("bob", "Hello")
    print(feed.get_feed("alice"))
