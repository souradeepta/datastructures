from python.advanced.trie import Trie


def test_exact_search_prefix_search_and_sorted_enumeration():
    trie = Trie()
    for word in ("banana", "app", "apple", "bat"):
        trie.insert(word)
    trie.insert("apple")

    assert trie.search("app")
    assert trie.search("apple")
    assert not trie.search("ap")
    assert trie.starts_with("ap")
    assert not trie.starts_with("car")
    assert trie.get_all_words() == ["app", "apple", "banana", "bat"]


def test_delete_leaf_prunes_only_unshared_branch():
    trie = Trie()
    for word in ("bat", "bar"):
        trie.insert(word)

    assert trie.delete("bar") is True
    assert trie.search("bat")
    assert not trie.search("bar")
    assert trie.starts_with("ba")
    assert not trie.starts_with("bar")
    assert trie.delete("bar") is False


def test_delete_prefix_word_returns_success_and_preserves_longer_word():
    trie = Trie()
    trie.insert("app")
    trie.insert("apple")

    assert trie.delete("app") is True
    assert not trie.search("app")
    assert trie.search("apple")
    assert trie.starts_with("app")
    assert trie.get_all_words() == ["apple"]


def test_delete_missing_word_does_not_change_contents():
    trie = Trie()
    trie.insert("cat")

    assert trie.delete("car") is False
    assert trie.get_all_words() == ["cat"]
