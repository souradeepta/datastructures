import pytest

from python.system_design.news_feed import NewsFeeder


def test_posts_have_monotonic_ids_and_multiple_posts_are_preserved():
    feed = NewsFeeder()

    first = feed.post("bob", "first")
    second = feed.post("bob", "second")

    assert first.id == 1
    assert second.post_id == 2
    assert feed.get_feed("bob") == [second, first]


def test_follow_is_idempotent_and_self_follow_is_rejected():
    feed = NewsFeeder()
    feed.follow("alice", "bob")
    feed.follow("alice", "bob")

    feed.post("bob", "hello")
    assert feed.get_feed("alice") == [feed.get_feed("bob")[0]]
    with pytest.raises(ValueError):
        feed.follow("bob", "bob")


def test_post_fans_out_to_author_and_current_distinct_followers():
    feed = NewsFeeder()
    feed.follow("alice", "bob")
    feed.follow("carol", "bob")
    feed.follow("alice", "bob")

    post = feed.post("bob", "hello")

    assert feed.get_feed("bob") == [post]
    assert feed.get_feed("alice") == [post]
    assert feed.get_feed("carol") == [post]


def test_following_is_prospective_and_feeds_are_reverse_chronological():
    feed = NewsFeeder()
    old_post = feed.post("bob", "old")
    feed.follow("alice", "bob")
    new_post = feed.post("bob", "new")

    assert feed.get_feed("alice") == [new_post]
    assert feed.get_feed("bob") == [new_post, old_post]


def test_feed_limit_and_result_state_are_isolated():
    feed = NewsFeeder()
    for content in ("one", "two", "three"):
        feed.post("bob", content)

    result = feed.get_feed("bob", limit=2)
    result.clear()
    exposed_feeds = feed.feeds
    exposed_feeds["bob"].clear()

    assert [post.content for post in feed.get_feed("bob")] == ["three", "two", "one"]
    with pytest.raises(ValueError):
        feed.get_feed("bob", -1)
    with pytest.raises(TypeError):
        feed.post("bob", object())
