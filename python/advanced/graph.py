"""
Graph (Directed & Undirected) — Adjacency List Representation
==============================================================
Supports both directed and undirected graphs with unweighted edges.
Vertices can be any hashable type.

Complexities  (V = vertices, E = edges):
    - add_vertex / add_edge / remove_edge: O(1) amortized
    - BFS / DFS:                           O(V + E)
    - has_cycle (undirected):              O(V + E)
    - has_cycle (directed, DFS color):     O(V + E)
    - topological_sort:                    O(V + E)
    - shortest_path (BFS, unweighted):     O(V + E)
    - Space:                               O(V + E)
"""

from __future__ import annotations
from collections import deque, defaultdict
from typing import Any, Dict, List, Optional, Set


def _ordered(values, reverse: bool = False) -> List[Any]:
    """Return comparable values sorted, with a safe fallback for opaque labels.

    Graph vertices only need to be hashable.  A graph containing a mixture of
    labels (or user-defined objects without ordering methods) must therefore
    not rely on ``sorted`` unconditionally.  The fallback keeps traversal
    deterministic for normal objects without imposing an ordering contract on
    callers.
    """
    values = list(values)
    try:
        return sorted(values, reverse=reverse)
    except TypeError:
        def sort_key(value: Any) -> tuple[str, str, str]:
            value_type = type(value)
            try:
                rendered = repr(value)
            except Exception:
                rendered = f"<object at {id(value):x}>"
            return (value_type.__module__, value_type.__qualname__, rendered)

        return sorted(values, key=sort_key, reverse=reverse)


class Graph:
    """
    Adjacency-list graph.

    Parameters
    ----------
    directed : bool
        If True, edges are one-directional (u → v).
        If False (default), each edge is stored in both directions.
    """

    def __init__(self, directed: bool = False) -> None:
        self._directed = directed
        # adjacency list: vertex → set of neighbours
        self._adj: Dict[Any, Set[Any]] = defaultdict(set)

    # ------------------------------------------------------------------
    # Mutation
    # ------------------------------------------------------------------

    def add_vertex(self, v: Any) -> None:
        """
        Ensure *v* exists in the graph (creates an isolated vertex if new).

        Time:  O(1)
        """
        if v not in self._adj:
            self._adj[v] = set()

    def add_edge(self, u: Any, v: Any) -> None:
        """
        Add an edge u → v (and v → u for undirected graphs).
        Auto-creates vertices if they don't exist.

        Time:  O(1)
        """
        self._adj[u].add(v)
        if not self._directed:
            self._adj[v].add(u)
        else:
            # Make sure v exists as a vertex even if it has no outgoing edges.
            if v not in self._adj:
                self._adj[v] = set()

    def remove_edge(self, u: Any, v: Any) -> None:
        """
        Remove the edge u → v (no-op if it doesn't exist).

        Time:  O(1)
        """
        if u not in self._adj:
            return
        self._adj[u].discard(v)
        if not self._directed and v in self._adj:
            self._adj[v].discard(u)

    @property
    def vertices(self) -> List[Any]:
        return list(self._adj.keys())

    @property
    def edges(self) -> List[tuple]:
        """Return all edges as (u, v) tuples (each undirected edge once)."""
        seen: Set[frozenset] = set()
        result = []
        for u, neighbours in self._adj.items():
            for v in neighbours:
                key = frozenset([u, v]) if not self._directed else (u, v)
                if key not in seen:
                    seen.add(key)
                    result.append((u, v))
        return result

    # ------------------------------------------------------------------
    # BFS
    # ------------------------------------------------------------------

    def bfs(self, start: Any) -> List[Any]:
        """
        Breadth-first traversal from *start*.
        Returns vertices in the order they are first visited.

        Time:  O(V + E)
        Space: O(V)
        """
        if start not in self._adj:
            return []
        visited: Set[Any] = {start}
        order: List[Any] = []
        queue: deque = deque([start])
        while queue:
            node = queue.popleft()
            order.append(node)
            for neighbour in _ordered(self._adj[node]):
                if neighbour not in visited:
                    visited.add(neighbour)
                    queue.append(neighbour)
        return order

    # ------------------------------------------------------------------
    # DFS
    # ------------------------------------------------------------------

    def dfs(self, start: Any) -> List[Any]:
        """
        Depth-first traversal from *start* (iterative).
        Returns vertices in the order they are first visited.

        Time:  O(V + E)
        Space: O(V)
        """
        if start not in self._adj:
            return []
        visited: Set[Any] = set()
        order: List[Any] = []
        stack = [start]
        while stack:
            node = stack.pop()
            if node in visited:
                continue
            visited.add(node)
            order.append(node)
            for neighbour in _ordered(self._adj[node], reverse=True):
                if neighbour not in visited:
                    stack.append(neighbour)
        return order

    # ------------------------------------------------------------------
    # Cycle detection
    # ------------------------------------------------------------------

    def has_cycle(self) -> bool:
        """
        Detect whether the graph contains a cycle.

        Undirected: DFS with parent tracking — back edge ⟹ cycle.
        Directed:   DFS three-colour algorithm (white/grey/black).
                    grey node reached again ⟹ cycle.

        Time:  O(V + E)
        Space: O(V)
        """
        if self._directed:
            return self._has_cycle_directed()
        return self._has_cycle_undirected()

    def _has_cycle_undirected(self) -> bool:
        visited: Set[Any] = set()

        def dfs(node: Any, parent: Any) -> bool:
            visited.add(node)
            for nb in self._adj[node]:
                if nb not in visited:
                    if dfs(nb, node):
                        return True
                elif nb != parent:
                    return True  # back edge to a non-parent ancestor
            return False

        for v in self._adj:
            if v not in visited:
                if dfs(v, None):
                    return True
        return False

    def _has_cycle_directed(self) -> bool:
        # 0 = white (unvisited), 1 = grey (in stack), 2 = black (done)
        color: Dict[Any, int] = {v: 0 for v in self._adj}

        def dfs(node: Any) -> bool:
            color[node] = 1  # grey
            for nb in self._adj[node]:
                if color[nb] == 1:
                    return True  # back edge
                if color[nb] == 0 and dfs(nb):
                    return True
            color[node] = 2  # black
            return False

        return any(dfs(v) for v in self._adj if color[v] == 0)

    # ------------------------------------------------------------------
    # Topological sort (Kahn's BFS-based algorithm)
    # ------------------------------------------------------------------

    def topological_sort(self) -> List[Any]:
        """
        Return a topological ordering of vertices (directed graphs only).
        Returns an empty list if the graph is not a DAG (cycle detected).

        Uses Kahn's algorithm (iterative, BFS-based).

        Time:  O(V + E)
        Space: O(V)
        """
        if not self._directed:
            raise ValueError("Topological sort is only defined for directed graphs.")

        in_degree: Dict[Any, int] = {v: 0 for v in self._adj}
        for v in self._adj:
            for nb in self._adj[v]:
                in_degree[nb] += 1

        queue: deque = deque(_ordered(v for v, d in in_degree.items() if d == 0))
        order: List[Any] = []

        while queue:
            node = queue.popleft()
            order.append(node)
            for nb in _ordered(self._adj[node]):
                in_degree[nb] -= 1
                if in_degree[nb] == 0:
                    queue.append(nb)

        if len(order) != len(self._adj):
            return []  # cycle detected
        return order

    # ------------------------------------------------------------------
    # Shortest path (BFS, unweighted)
    # ------------------------------------------------------------------

    def shortest_path(self, start: Any, end: Any) -> Optional[List[Any]]:
        """
        Return the shortest path from *start* to *end* as a list of vertices,
        or None if no path exists.

        Works for both directed and undirected unweighted graphs.
        For weighted graphs, use Dijkstra's algorithm instead.

        Time:  O(V + E)
        Space: O(V)
        """
        if start not in self._adj or end not in self._adj:
            return None
        if start == end:
            return [start]

        visited: Set[Any] = {start}
        # Store full path in queue to simplify reconstruction.
        queue: deque = deque([[start]])

        while queue:
            path = queue.popleft()
            node = path[-1]
            for nb in _ordered(self._adj[node]):
                if nb == end:
                    return path + [nb]
                if nb not in visited:
                    visited.add(nb)
                    queue.append(path + [nb])
        return None

    # ------------------------------------------------------------------
    # String representation
    # ------------------------------------------------------------------

    def __str__(self) -> str:
        kind = "Directed" if self._directed else "Undirected"
        lines = [f"{kind} Graph (V={len(self._adj)}, E={len(self.edges)}):"]
        for v in sorted(self._adj.keys(), key=str):
            neighbours = ", ".join(str(nb) for nb in sorted(self._adj[v], key=str))
            arrow = "→" if self._directed else "—"
            lines.append(f"  {v} {arrow} [{neighbours}]")
        return "\n".join(lines)


# ----------------------------------------------------------------------
# Demo
# ----------------------------------------------------------------------

if __name__ == "__main__":
    print("=== Undirected Graph ===")
    g = Graph(directed=False)
    edges = [(1, 2), (1, 3), (2, 4), (3, 4), (4, 5)]
    for u, v in edges:
        g.add_edge(u, v)
    print(g)
    print("BFS from 1:", g.bfs(1))
    print("DFS from 1:", g.dfs(1))
    print("Has cycle? :", g.has_cycle())
    print("Shortest path 1→5:", g.shortest_path(1, 5))

    print()
    print("=== Directed Graph (DAG) ===")
    dag = Graph(directed=True)
    dag_edges = [
        ("A", "B"), ("A", "C"), ("B", "D"),
        ("C", "D"), ("D", "E"), ("B", "E"),
    ]
    for u, v in dag_edges:
        dag.add_edge(u, v)
    print(dag)
    print("BFS from A    :", dag.bfs("A"))
    print("DFS from A    :", dag.dfs("A"))
    print("Has cycle?    :", dag.has_cycle())
    print("Topo sort     :", dag.topological_sort())
    print("Shortest A→E  :", dag.shortest_path("A", "E"))

    print()
    print("=== Directed Graph with Cycle ===")
    cyc = Graph(directed=True)
    cyc.add_edge(1, 2)
    cyc.add_edge(2, 3)
    cyc.add_edge(3, 1)  # cycle
    print(cyc)
    print("Has cycle?    :", cyc.has_cycle())
    print("Topo sort     :", cyc.topological_sort(), "(empty = cycle detected)")
