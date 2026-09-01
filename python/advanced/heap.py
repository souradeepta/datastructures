"""
Min-Heap and Max-Heap (Array-based)
=====================================
A complete binary tree stored as an array where every parent satisfies the
heap property. The MinHeap always has the smallest element at the root;
the MaxHeap always has the largest.

Array indexing (1-based logic mapped to 0-based array):
    parent(i) = (i - 1) // 2
    left(i)   = 2*i + 1
    right(i)  = 2*i + 2

Complexities:
    - push (heapify-up):     O(log n)
    - pop  (heapify-down):   O(log n)
    - peek:                  O(1)
    - build_heap from list:  O(n)   ← Floyd's algorithm
    - heap_sort:             O(n log n), O(1) extra space
    - Space:                 O(n)
"""

from __future__ import annotations
from typing import List, TypeVar, Generic, Callable, Optional

T = TypeVar("T")


class MinHeap(Generic[T]):
    """
    Min-Heap: parent <= children at every node.
    Supports any type with a total ordering (``<``).
    """

    def __init__(self) -> None:
        self._data: List[T] = []

    # ------------------------------------------------------------------
    # Core helpers
    # ------------------------------------------------------------------

    def _swap(self, i: int, j: int) -> None:
        self._data[i], self._data[j] = self._data[j], self._data[i]

    @staticmethod
    def _parent(i: int) -> int:
        return (i - 1) // 2

    @staticmethod
    def _left(i: int) -> int:
        return 2 * i + 1

    @staticmethod
    def _right(i: int) -> int:
        return 2 * i + 2

    # ------------------------------------------------------------------
    # Sift operations
    # ------------------------------------------------------------------

    def heapify_up(self, i: int) -> None:
        """
        Restore the heap property upward from index *i*.

        Called after inserting at the end.
        Time:  O(log n)
        """
        while i > 0:
            p = self._parent(i)
            if self._data[i] < self._data[p]:
                self._swap(i, p)
                i = p
            else:
                break

    def heapify_down(self, i: int) -> None:
        """
        Restore the heap property downward from index *i*.

        Called after replacing root with the last element.
        Time:  O(log n)
        """
        n = len(self._data)
        while True:
            smallest = i
            l, r = self._left(i), self._right(i)
            if l < n and self._data[l] < self._data[smallest]:
                smallest = l
            if r < n and self._data[r] < self._data[smallest]:
                smallest = r
            if smallest == i:
                break
            self._swap(i, smallest)
            i = smallest

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def push(self, val: T) -> None:
        """
        Insert *val* into the heap.

        Time:  O(log n)
        Space: O(1) amortized
        """
        self._data.append(val)
        self.heapify_up(len(self._data) - 1)

    def pop(self) -> T:
        """
        Remove and return the minimum element.

        Time:  O(log n)
        Raises IndexError if the heap is empty.
        """
        if not self._data:
            raise IndexError("pop from empty heap")
        # Swap root with last, remove last, sift down new root.
        self._swap(0, len(self._data) - 1)
        val = self._data.pop()
        if self._data:
            self.heapify_down(0)
        return val

    def peek(self) -> T:
        """
        Return (without removing) the minimum element.

        Time:  O(1)
        Raises IndexError if the heap is empty.
        """
        if not self._data:
            raise IndexError("peek at empty heap")
        return self._data[0]

    def build_heap(self, data: List[T]) -> None:
        """
        Build a heap in-place from an arbitrary list.

        Uses Floyd's algorithm: start from the last internal node and
        sift each one down. This is O(n) — provably better than n pushes.

        Time:  O(n)
        Space: O(1) extra (operates on a copy stored internally)
        """
        self._data = list(data)
        n = len(self._data)
        # Last internal node index = (n // 2) - 1
        for i in range(n // 2 - 1, -1, -1):
            self.heapify_down(i)

    def heap_sort(self, data: List[T]) -> List[T]:
        """
        Sort *data* in ascending order using heap sort.

        Builds a MinHeap and pops repeatedly — O(n log n), O(n) space.
        For O(1) extra-space in-place sort, a MaxHeap variant is typical
        (see MaxHeap.heap_sort).

        Time:  O(n log n)
        Space: O(n)
        """
        self.build_heap(data)
        return [self.pop() for _ in range(len(self._data))]

    def __len__(self) -> int:
        return len(self._data)

    def __bool__(self) -> bool:
        return bool(self._data)

    def __repr__(self) -> str:
        return f"MinHeap({self._data})"


class MaxHeap(Generic[T]):
    """
    Max-Heap: parent >= children at every node.
    Supports any type with a total ordering (``>``).
    """

    def __init__(self) -> None:
        self._data: List[T] = []

    def _swap(self, i: int, j: int) -> None:
        self._data[i], self._data[j] = self._data[j], self._data[i]

    @staticmethod
    def _parent(i: int) -> int:
        return (i - 1) // 2

    @staticmethod
    def _left(i: int) -> int:
        return 2 * i + 1

    @staticmethod
    def _right(i: int) -> int:
        return 2 * i + 2

    def heapify_up(self, i: int) -> None:
        """
        Restore max-heap property upward.

        Time:  O(log n)
        """
        while i > 0:
            p = self._parent(i)
            if self._data[i] > self._data[p]:
                self._swap(i, p)
                i = p
            else:
                break

    def heapify_down(self, i: int) -> None:
        """
        Restore max-heap property downward.

        Time:  O(log n)
        """
        n = len(self._data)
        while True:
            largest = i
            l, r = self._left(i), self._right(i)
            if l < n and self._data[l] > self._data[largest]:
                largest = l
            if r < n and self._data[r] > self._data[largest]:
                largest = r
            if largest == i:
                break
            self._swap(i, largest)
            i = largest

    def push(self, val: T) -> None:
        """
        Insert *val*.

        Time:  O(log n)
        """
        self._data.append(val)
        self.heapify_up(len(self._data) - 1)

    def pop(self) -> T:
        """
        Remove and return the maximum element.

        Time:  O(log n)
        """
        if not self._data:
            raise IndexError("pop from empty heap")
        self._swap(0, len(self._data) - 1)
        val = self._data.pop()
        if self._data:
            self.heapify_down(0)
        return val

    def peek(self) -> T:
        """
        Return (without removing) the maximum element.

        Time:  O(1)
        """
        if not self._data:
            raise IndexError("peek at empty heap")
        return self._data[0]

    def build_heap(self, data: List[T]) -> None:
        """
        Build a max-heap in O(n) via Floyd's algorithm.

        Time:  O(n)
        """
        self._data = list(data)
        n = len(self._data)
        for i in range(n // 2 - 1, -1, -1):
            self.heapify_down(i)

    def heap_sort(self, data: List[T]) -> List[T]:
        """
        In-place ascending heap sort using a MaxHeap.

        Classic O(n log n), O(1) extra-space approach:
          1. Build max-heap.
          2. For each position from end, swap root (max) to that position,
             shrink the heap by 1, and sift down the new root.

        Time:  O(n log n)
        Space: O(1) extra (works on a copy)
        """
        arr = list(data)
        n = len(arr)

        # Build max-heap in arr.
        for i in range(n // 2 - 1, -1, -1):
            self._sift_down_arr(arr, i, n)

        # Extract max repeatedly.
        for end in range(n - 1, 0, -1):
            arr[0], arr[end] = arr[end], arr[0]
            self._sift_down_arr(arr, 0, end)

        return arr

    @staticmethod
    def _sift_down_arr(arr: list, i: int, size: int) -> None:
        """Sift-down on a raw list with explicit size (for heap_sort)."""
        while True:
            largest = i
            l, r = 2 * i + 1, 2 * i + 2
            if l < size and arr[l] > arr[largest]:
                largest = l
            if r < size and arr[r] > arr[largest]:
                largest = r
            if largest == i:
                break
            arr[i], arr[largest] = arr[largest], arr[i]
            i = largest

    def __len__(self) -> int:
        return len(self._data)

    def __bool__(self) -> bool:
        return bool(self._data)

    def __repr__(self) -> str:
        return f"MaxHeap({self._data})"


# ----------------------------------------------------------------------
# Demo
# ----------------------------------------------------------------------

if __name__ == "__main__":
    data = [3, 1, 4, 1, 5, 9, 2, 6, 5, 3]
    print("=== Heap Demo ===")
    print("Input:", data)

    # MinHeap
    min_h = MinHeap()
    min_h.build_heap(data)
    print("\nMinHeap internal array:", min_h)
    print("Peek (min):", min_h.peek())
    pops = [min_h.pop() for _ in range(len(min_h))]
    print("Pop-all order (ascending):", pops)

    # MaxHeap
    max_h = MaxHeap()
    max_h.build_heap(data)
    print("\nMaxHeap internal array:", max_h)
    print("Peek (max):", max_h.peek())
    pops = [max_h.pop() for _ in range(len(max_h))]
    print("Pop-all order (descending):", pops)

    # heap_sort
    max_h2 = MaxHeap()
    sorted_asc = max_h2.heap_sort(data)
    print("\nheap_sort ascending:", sorted_asc)
