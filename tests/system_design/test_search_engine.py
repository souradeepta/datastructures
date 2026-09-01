from python.system_design.search_engine import SearchEngine


def test_search_normalizes_case_punctuation_and_supports_and_queries():
    engine = SearchEngine()
    engine.index_doc(1, "Python, patterns and testing")
    engine.index_doc(2, "Testing Python systems")
    engine.index_doc(3, "Python only")

    assert engine.search("python") == [1, 2, 3]
    assert engine.search("PYTHON testing") == [1, 2]
    assert engine.search("testing, python python") == [1, 2]
    assert engine.search("unknown") == []
    assert engine.search("   !!!") == []


def test_reindexing_removes_stale_terms_and_preserves_document_order():
    engine = SearchEngine()
    engine.index_doc("first", "red apple")
    engine.index_doc("second", "red banana")
    engine.index_doc("first", "green apple")

    assert engine.search("red") == ["second"]
    assert engine.search("apple") == ["first"]
    assert engine.search("apple green") == ["first"]
    assert engine.search("banana red") == ["second"]


def test_document_removal_and_result_isolation():
    engine = SearchEngine()
    engine.index_doc(1, "shared term")
    engine.index_doc(2, "shared term")

    result = engine.search("shared")
    result.append(99)
    assert engine.search("shared") == [1, 2]
    assert engine.remove_doc(1)
    assert engine.search("shared") == [2]
    assert not engine.remove_doc(1)
