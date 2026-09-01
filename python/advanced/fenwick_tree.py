"""
Fenwick Tree (Binary Indexed Tree — BIT)
==========================================
A clever array-based structure for prefix-sum queries and point updates.
Each index i is responsible for a range of elements determined by its lowest
set bit (LSB): the range length equals LSB(i) = i & (-i).

Navigation:
    - To move to the parent (for update): i += i & (-i)   # add LSB
    - To move to the responsible prefix  (for query): i -= i & (-i)   # remove LSB

This file uses **1-based indexing** (standard BIT convention).
External API uses 0-based indexes for Python friendliness.

Complexities:
    - update(i, delta):   O(log n)
    - prefix_sum(i):      O(log n)
    - range_query(l, r):  O(log n)   [two prefix_sum calls]
    - build from list:    O(n log n)  [n updates], or O(n) with the trick below
    - Space:              O(n)
"""

from __future__ import annotations
from typing import List


class FenwickTree:
    """
    Binary Indexed Tree for prefix-sum queries and point updates.

    All external indices are 0-based.
    Internally uses 1-based indices for correct LSB arithmetic.
    """

    def __init__(self, n: int) -> None:
        """
        Create an empty BIT of size *n*.

        Time:  O(n)
        """
        if not isinstance(n, int) or isinstance(n, bool) or n < 0:
            raise ValueError("Fenwick tree size must be a non-negative integer")
        self._n = n
        self._tree: List[int] = [0] * (n + 1)  # 1-indexed; index 0 unused

    # ------------------------------------------------------------------
    # Core operations
    # ------------------------------------------------------------------

    def update(self, i: int, delta: int) -> None:
        """
        Add *delta* to position *i* (0-based).

        Internally traverses upward by adding the LSB repeatedly:
            i, i + (i & -i), ...

        BIT Bit Trick:
            i & (-i) isolates the lowest set bit.
            Adding it moves i to the next node that is responsible for
            a range that includes the original i.

        Time:  O(log n)

        Example for n=8, i=3 (1-based=4, binary=0100):
            Step 1: pos=4  (0100), update tree[4]
            Step 2: pos=8  (1000), update tree[8]   (+4 = add LSB 0100)
            (8 > n=8? no, so done)
        """
        self._validate_index(i)
        pos = i + 1  # convert to 1-based
        while pos <= self._n:
            self._tree[pos] += delta
            # Move to next responsible ancestor.
            pos += pos & (-pos)  # add lowest set bit

    def prefix_sum(self, i: int) -> int:
        """
        Return the sum of arr[0..i] (inclusive, 0-based).

        Traverses downward by removing the LSB:
            i, i - (i & -i), ...

        BIT Bit Trick:
            i & (-i) isolates the lowest set bit.
            Removing it moves i to the parent in the BIT sense —
            the node whose range ends just before this one begins.

        Time:  O(log n)

        Example for i=6 (1-based=7, binary=0111):
            Step 1: pos=7  (0111), accumulate tree[7]
            Step 2: pos=6  (0110), accumulate tree[6]  (-1 = remove LSB 0001)
            Step 3: pos=4  (0100), accumulate tree[4]  (-2 = remove LSB 0010)
            Step 4: pos=0, stop.
        """
        self._validate_index(i)
        total = 0
        pos = i + 1  # convert to 1-based
        while pos > 0:
            total += self._tree[pos]
            # Move to parent — strip lowest set bit.
            pos -= pos & (-pos)  # remove lowest set bit
        return total

    def range_query(self, l: int, r: int) -> int:
        """
        Return the sum of arr[l..r] (inclusive, 0-based).

        Uses the identity: sum(l, r) = prefix_sum(r) - prefix_sum(l-1).

        Time:  O(log n)
        """
        if l > r:
            raise ValueError(f"l={l} must be <= r={r}")
        self._validate_index(l)
        self._validate_index(r)
        if l == 0:
            return self.prefix_sum(r)
        return self.prefix_sum(r) - self.prefix_sum(l - 1)

    # ------------------------------------------------------------------
    # Build from existing list
    # ------------------------------------------------------------------

    @classmethod
    def build(cls, data: List[int]) -> "FenwickTree":
        """
        Build a Fenwick Tree from a list in O(n) time.

        Faster O(n) trick: directly compute tree[i] = partial sum
        that each index is responsible for, rather than calling update n times.

        Time:  O(n)
        Space: O(n)
        """
        n = len(data)
        ft = cls(n)
        # Copy data into 1-indexed positions.
        for i in range(1, n + 1):
            ft._tree[i] = data[i - 1]
        # Propagate each position's value to its parent.
        for i in range(1, n + 1):
            parent = i + (i & (-i))   # add lowest set bit → parent
            if parent <= n:
                ft._tree[parent] += ft._tree[i]
        return ft

    # ------------------------------------------------------------------
    # Point-value accessor
    # ------------------------------------------------------------------

    def point_value(self, i: int) -> int:
        """
        Return the current value at index *i* in O(log n) via two prefix queries.

        Time:  O(log n)
        """
        self._validate_index(i)
        if i == 0:
            return self.prefix_sum(0)
        return self.prefix_sum(i) - self.prefix_sum(i - 1)

    def _validate_index(self, i: int) -> None:
        if not isinstance(i, int) or isinstance(i, bool) or not 0 <= i < self._n:
            raise IndexError(f"Index {i} out of range [0, {self._n - 1}]")

    # ------------------------------------------------------------------
    # String representation
    # ------------------------------------------------------------------

    def __repr__(self) -> str:
        return f"FenwickTree(n={self._n}, internal={self._tree[1:]})"


# ----------------------------------------------------------------------
# Application: Kruskal's MST helper (no actual graph — conceptual demo)
# ----------------------------------------------------------------------

def count_inversions(arr: List[int]) -> int:
    """
    Count inversions in *arr* using a Fenwick Tree.

    An inversion is a pair (i, j) with i < j and arr[i] > arr[j].
    Useful in merge-sort-based counting but BIT gives a cleaner solution.

    Time:  O(n log n)
    Space: O(n)
    """
    if not arr:
        return 0
    ranks = {value: rank for rank, value in enumerate(sorted(set(arr)))}
    ft = FenwickTree(len(ranks))
    inversions = 0
    for val in arr:
        rank = ranks[val]
        # Count elements already inserted that are greater than val.
        inversions += ft.range_query(rank + 1, len(ranks) - 1) if rank + 1 < len(ranks) else 0
        ft.update(rank, 1)
    return inversions


# ----------------------------------------------------------------------
# Demo
# ----------------------------------------------------------------------

if __name__ == "__main__":
    print("=== Fenwick Tree (BIT) ===")
    data = [1, 7, 3, 0, 7, 8, 3, 2, 6, 2]
    print("Data:", data)

    ft = FenwickTree.build(data)
    print()
    print("prefix_sum(0)  :", ft.prefix_sum(0))   # 1
    print("prefix_sum(4)  :", ft.prefix_sum(4))   # 18
    print("prefix_sum(9)  :", ft.prefix_sum(9))   # 39
    print()
    print("range_query(2,5):", ft.range_query(2, 5))   # 3+0+7+8 = 18
    print("range_query(0,9):", ft.range_query(0, 9))   # 39

    print()
    print("Updating index 3: value 0 → 5 (delta=+5)")
    ft.update(3, 5)
    print("range_query(2,5):", ft.range_query(2, 5))   # 3+5+7+8 = 23
    print("prefix_sum(9)   :", ft.prefix_sum(9))        # 44

    print()
    print("=== Inversion Count ===")
    inv_arr = [8, 4, 2, 1]
    print(f"Inversions in {inv_arr}:", count_inversions(inv_arr))  # 6

    inv_arr2 = [3, 1, 2]
    print(f"Inversions in {inv_arr2}:", count_inversions(inv_arr2))  # 2

    print()
    print("Internal BIT array:", ft)
