"""
Disjoint Set Union (DSU / Union-Find)
=======================================
A data structure that maintains a collection of disjoint (non-overlapping)
sets and supports two efficient operations:
    - find(x):     Determine which set *x* belongs to (returns representative).
    - union(x, y): Merge the sets containing *x* and *y*.

Two key optimizations:
    1. Path Compression (in find):  Flatten the tree so every node points
       directly to the root after a find call.
    2. Union by Rank (in union):    Always attach the smaller tree under the
       root of the taller tree to keep trees shallow.

With both optimizations, operations run in nearly O(1) amortized time:
    - find / union: O(α(n))  where α is the inverse-Ackermann function,
                              which is <= 4 for all practical n.
    - Space:        O(n)

Classic use cases:
    - Kruskal's Minimum Spanning Tree algorithm.
    - Detecting cycles in undirected graphs.
    - Connected components.
    - Network connectivity queries.
"""

from __future__ import annotations
from typing import Any, Dict, List, Optional, Tuple


class UnionFind:
    """
    Disjoint Set Union with path compression and union by rank.

    Supports any hashable element type (int, str, etc.).
    """

    def __init__(self) -> None:
        # parent[x] = representative of x's set (initially x itself).
        self._parent: Dict[Any, Any] = {}
        # rank[x] = upper bound on the height of x's subtree.
        self._rank: Dict[Any, int] = {}
        # Number of distinct sets.
        self._num_components: int = 0

    # ------------------------------------------------------------------
    # Make set
    # ------------------------------------------------------------------

    def add(self, x: Any) -> None:
        """
        Explicitly add element *x* to its own singleton set.
        No-op if *x* is already present.

        Time:  O(1)
        """
        if x not in self._parent:
            self._parent[x] = x
            self._rank[x] = 0
            self._num_components += 1

    def _ensure(self, x: Any) -> None:
        """Auto-add *x* if not present (lazy initialization)."""
        if x not in self._parent:
            self.add(x)

    # ------------------------------------------------------------------
    # Find (with path compression)
    # ------------------------------------------------------------------

    def find(self, x: Any) -> Any:
        """
        Return the representative (root) of the set containing *x*.

        Path Compression: on the way back up the recursion, every node on
        the path is made to point directly to the root.  This flattens the
        tree so future finds are O(1).

        Time:  O(α(n)) amortized
        """
        self._ensure(x)
        if self._parent[x] != x:
            # Recursive path compression: point x directly to root.
            self._parent[x] = self.find(self._parent[x])
        return self._parent[x]

    # ------------------------------------------------------------------
    # Union (by rank)
    # ------------------------------------------------------------------

    def union(self, x: Any, y: Any) -> bool:
        """
        Merge the sets containing *x* and *y*.
        Returns True if they were in different sets (merge happened),
        False if they were already in the same set.

        Union by Rank: attach the root with lower rank under the root with
        higher rank.  When ranks are equal, arbitrarily choose one root and
        increment its rank.  This keeps tree heights O(log n) without
        path compression, and nearly O(1) with it.

        Time:  O(α(n)) amortized
        """
        rx, ry = self.find(x), self.find(y)
        if rx == ry:
            return False  # already connected

        # Attach smaller rank tree under larger rank tree.
        if self._rank[rx] < self._rank[ry]:
            rx, ry = ry, rx  # ensure rx has the higher (or equal) rank
        self._parent[ry] = rx
        if self._rank[rx] == self._rank[ry]:
            self._rank[rx] += 1

        self._num_components -= 1
        return True

    # ------------------------------------------------------------------
    # Queries
    # ------------------------------------------------------------------

    def connected(self, x: Any, y: Any) -> bool:
        """
        Return True if *x* and *y* belong to the same set.

        Time:  O(α(n)) amortized
        """
        return self.find(x) == self.find(y)

    @property
    def num_components(self) -> int:
        """Number of distinct sets currently in the structure."""
        return self._num_components

    def component_of(self, x: Any) -> List[Any]:
        """
        Return all elements in the same set as *x*.

        Time:  O(n)  — iterates all elements.
        """
        root = self.find(x)
        return [e for e in self._parent if self.find(e) == root]

    def all_components(self) -> List[List[Any]]:
        """
        Return a list of lists, each being one connected component.

        Time:  O(n α(n))
        """
        groups: Dict[Any, List[Any]] = {}
        for e in self._parent:
            root = self.find(e)
            groups.setdefault(root, []).append(e)
        return list(groups.values())

    def __repr__(self) -> str:
        comps = self.all_components()
        return f"UnionFind(components={comps})"


# ----------------------------------------------------------------------
# Application: Kruskal's Minimum Spanning Tree
# ----------------------------------------------------------------------

def kruskal_mst(
    vertices: List[Any],
    edges: List[Tuple[int, Any, Any]],
) -> Tuple[List[Tuple[int, Any, Any]], int]:
    """
    Kruskal's algorithm for Minimum Spanning Tree.

    Parameters
    ----------
    vertices : list
        All vertex labels.
    edges : list of (weight, u, v)
        All edges as (weight, u, v) tuples.

    Returns
    -------
    mst_edges : list of (weight, u, v) in the MST
    total_weight : int

    Algorithm:
        1. Sort all edges by weight (greedy).
        2. For each edge (u, v), if u and v are in different components,
           add the edge to MST and union them.
        3. Stop when MST has V-1 edges.

    Time:  O(E log E) dominated by sorting.
    Space: O(V)
    """
    uf = UnionFind()
    for v in vertices:
        uf.add(v)

    mst_edges = []
    total_weight = 0

    for weight, u, v in sorted(edges, key=lambda edge: edge[0]):  # sort by weight
        if uf.union(u, v):              # no cycle
            mst_edges.append((weight, u, v))
            total_weight += weight
            if len(mst_edges) == len(vertices) - 1:
                break  # MST complete

    return mst_edges, total_weight


# ----------------------------------------------------------------------
# Demo
# ----------------------------------------------------------------------

if __name__ == "__main__":
    print("=== Union-Find ===")
    uf = UnionFind()
    for x in range(1, 8):
        uf.add(x)

    unions = [(1, 2), (2, 3), (4, 5), (6, 7)]
    for a, b in unions:
        uf.union(a, b)
        print(f"union({a}, {b})")

    print()
    print("connected(1, 3):", uf.connected(1, 3))  # True
    print("connected(1, 4):", uf.connected(1, 4))  # False
    print("num_components :", uf.num_components)   # 4
    print("all_components :", sorted(sorted(c) for c in uf.all_components()))

    uf.union(3, 4)
    print("\nAfter union(3, 4):")
    print("connected(1, 5):", uf.connected(1, 5))  # True
    print("num_components :", uf.num_components)   # 3

    print()
    print("=== Kruskal's MST ===")
    vertices = ["A", "B", "C", "D", "E"]
    edges = [
        (1, "A", "B"),
        (3, "A", "C"),
        (4, "B", "C"),
        (2, "B", "D"),
        (5, "C", "E"),
        (7, "D", "E"),
        (6, "B", "E"),
    ]
    mst, cost = kruskal_mst(vertices, edges)
    print("MST edges (weight, u, v):")
    for w, u, v in mst:
        print(f"  {u} — {v}  (weight={w})")
    print("Total MST cost:", cost)
