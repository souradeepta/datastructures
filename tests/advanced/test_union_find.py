from python.advanced.union_find import UnionFind, kruskal_mst


def test_add_is_idempotent_and_find_is_lazy():
    uf = UnionFind()
    uf.add("a")
    uf.add("a")
    assert uf.num_components == 1

    assert uf.find("b") == "b"
    assert uf.num_components == 2
    assert uf.connected("b", "b")


def test_union_returns_whether_a_merge_happened_and_tracks_components():
    uf = UnionFind()

    assert uf.union("a", "b") is True
    assert uf.union("a", "b") is False
    assert uf.union("b", "c") is True
    assert uf.num_components == 1
    assert uf.connected("a", "c")
    assert sorted(uf.component_of("b")) == ["a", "b", "c"]
    assert {frozenset(component) for component in uf.all_components()} == {
        frozenset({"a", "b", "c"})
    }


def test_find_compresses_a_multi_level_parent_chain():
    uf = UnionFind()
    for value in ("a", "b", "c", "d"):
        uf.add(value)
    uf.union("a", "b")
    uf.union("c", "d")
    uf.union("a", "c")

    assert uf._parent["d"] == "c"
    assert uf.find("d") == "a"
    assert uf._parent["d"] == "a"


def test_kruskal_finds_mst_and_skips_cycle_edge():
    vertices = ["a", "b", "c"]
    edges = [(10, "a", "c"), (2, "b", "c"), (1, "a", "b")]

    mst, total_weight = kruskal_mst(vertices, edges)

    assert mst == [(1, "a", "b"), (2, "b", "c")]
    assert total_weight == 3
    assert len(mst) == len(vertices) - 1


def test_kruskal_returns_minimum_spanning_forest_for_disconnected_graph():
    vertices = ["a", "b", "c", "d"]
    edges = [(4, "a", "b"), (1, "a", "b"), (2, "c", "d")]

    mst, total_weight = kruskal_mst(vertices, edges)

    assert mst == [(1, "a", "b"), (2, "c", "d")]
    assert total_weight == 3


class UnorderableVertex:
    def __init__(self, name):
        self.name = name

    def __hash__(self):
        return hash(self.name)

    def __eq__(self, other):
        return isinstance(other, UnorderableVertex) and self.name == other.name


def test_kruskal_equal_weights_do_not_compare_vertex_labels():
    a = UnorderableVertex("a")
    b = UnorderableVertex("b")
    c = UnorderableVertex("c")

    mst, total_weight = kruskal_mst(
        [a, b, c],
        [(1, a, b), (1, b, c), (2, a, c)],
    )

    assert len(mst) == 2
    assert total_weight == 2
