from python.advanced_ds.suffix_tree import SuffixTree


def test_search_returns_all_occurrences():
    assert SuffixTree("banana").search("ana") == [1, 3]


def test_longest_repeated_substring():
    assert SuffixTree("banana").longest_repeated_substring() == "ana"
    assert SuffixTree("aaaa").longest_repeated_substring() == "aaa"


def test_no_repeated_substring_returns_empty_string():
    assert SuffixTree("abc").longest_repeated_substring() == ""
