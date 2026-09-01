import pytest

from python.advanced.graph import Graph


def test_undirected_edges_traversals_and_mutation():
    graph = Graph()
    graph.add_edge(1, 2)
    graph.add_edge(1, 3)
    graph.add_edge(2, 4)
    graph.add_vertex(5)

    assert graph.bfs(1) == [1, 2, 3, 4]
    assert graph.dfs(1) == [1, 2, 4, 3]
    assert graph.shortest_path(1, 4) == [1, 2, 4]
    assert graph.shortest_path(1, 5) is None
    assert not graph.has_cycle()

    graph.add_edge(3, 4)
    assert graph.has_cycle()
    graph.remove_edge(3, 4)
    assert not graph.has_cycle()


def test_directed_topological_sort_and_cycle_detection():
    graph = Graph(directed=True)
    graph.add_edge("A", "C")
    graph.add_edge("A", "B")
    graph.add_edge("B", "D")
    graph.add_edge("C", "D")

    assert graph.topological_sort() == ["A", "B", "C", "D"]
    assert graph.shortest_path("A", "D") == ["A", "B", "D"]
    assert not graph.has_cycle()

    graph.add_edge("D", "A")
    assert graph.has_cycle()
    assert graph.topological_sort() == []

    with pytest.raises(ValueError):
        Graph().topological_sort()


def test_opaque_hashable_vertices_do_not_require_ordering():
    class Vertex:
        def __init__(self, name):
            self.name = name

        def __hash__(self):
            return hash(self.name)

        def __eq__(self, other):
            return isinstance(other, Vertex) and self.name == other.name

        def __repr__(self):
            return f"Vertex({self.name!r})"

    start, left, right = Vertex("start"), Vertex("left"), Vertex("right")
    graph = Graph(directed=True)
    graph.add_edge(start, right)
    graph.add_edge(start, left)

    assert set(graph.bfs(start)) == {start, left, right}
    assert set(graph.dfs(start)) == {start, left, right}
    order = graph.topological_sort()
    assert order.index(start) < order.index(left)
    assert order.index(start) < order.index(right)
    assert graph.shortest_path(start, left) == [start, left]


def test_removing_missing_edge_does_not_create_vertices():
    graph = Graph()
    graph.remove_edge("missing", "also-missing")
    assert graph.vertices == []

    graph.add_vertex("known")
    graph.remove_edge("known", "missing")
    assert graph.vertices == ["known"]
