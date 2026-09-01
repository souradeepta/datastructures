# Algorithms — Complete Implementation Reference

Algorithms organized by category with Python implementations and tests in the repository's
`python/algorithms/` and `tests/algorithms/` trees. Java is not currently part of the maintained tree.

---

## 📚 Algorithm Categories

### 🔤 Sorting & Searching
- **[Sorting Algorithms](sorting/)** — Bubble, selection, insertion, merge, quick, heap, counting, radix
- **[Searching Algorithms](searching/)** — Linear search, binary search, variations

### 🧮 Dynamic Programming
- **[DP Patterns](dp/)** — Fibonacci, coin change, knapsack, LCS, LIS, edit distance, matrix chain

### 📊 Graph Algorithms
- **[Graph Fundamentals](graphs/)** — BFS, DFS, topological sort, cycle detection
- **[Advanced Graph](graphs/advanced/)** — Dijkstra, Bellman-Ford, MST (Kruskal, Prim), Floyd-Warshall

### 🔤 String Algorithms
- **[String Matching](string-algorithms/)** — KMP, Z-algorithm, Rabin-Karp, suffix arrays

### 🎯 Greedy Algorithms
- **[Greedy Patterns](greedy/)** — Activity selection, fractional knapsack, Huffman coding

### 🔢 Math & Number Theory
- **[Math Fundamentals](math/)** — GCD, LCM, prime checking, modular arithmetic, combinatorics

### 🎨 Bit Manipulation
- **[Bit Techniques](bit-manipulation/)** — AND, OR, XOR tricks, bit counting, subset generation

### 📐 Geometry
- **[Geometry Basics](geometry/)** — Coordinate geometry, distance, area, line intersection

---

## 🎯 Quick Access

| Algorithm | Difficulty | Time | Space | Guide | Python | Tests |
|-----------|-----------|------|-------|-------|--------|-------|
| Bubble Sort | Easy | O(n²) | O(1) | [Guide](sorting/) | [Python](../../python/algorithms/sorting/sorting.py) | [Tests](../../tests/algorithms/test_sorting.py) |
| Merge Sort | Medium | O(n log n) | O(n) | [Guide](sorting/) | [Python](../../python/algorithms/sorting/sorting.py) | [Tests](../../tests/algorithms/test_sorting.py) |
| Binary Search | Medium | O(log n) | O(1) | [Guide](searching/) | [Python](../../python/algorithms/searching/searching.py) | [Tests](../../tests/algorithms/test_searching.py) |
| Dynamic Programming | Hard | Varies | Varies | [Guide](dp/) | [Python](../../python/algorithms/dp/dp.py) | [Tests](../../tests/algorithms/test_dp.py) |
| Graph BFS/DFS | Medium | O(V+E) | O(V) | [Guide](graphs/) | [Python](../../python/algorithms/graph/graph_algorithms.py) | [Tests](../../tests/algorithms/test_graph.py) |
| Dijkstra | Hard | O((V+E)logV) | O(V) | [Guide](graphs/advanced/) | [Python](../../python/algorithms/graph/graph_algorithms.py) | [Tests](../../tests/algorithms/test_graph.py) |
| KMP String Match | Hard | O(n+m) | O(m) | [Guide](string-algorithms/) | [Python](../../python/algorithms/string/string_algorithms.py) | — |

---

## 🚀 Learning Path

### Beginner Week
1. Sorting (bubble, selection, insertion)
2. Searching (linear, binary)
3. Basic DP (Fibonacci, coin change)

### Intermediate Week
4. Graph basics (BFS, DFS)
5. More DP (knapsack, LCS)
6. String algorithms

### Advanced Week
7. Advanced graph (Dijkstra, MST)
8. Bit manipulation tricks
9. Complex DP (matrix chain)

---

## 📁 Repository Structure

```
docs/05-algorithms/
├── README.md (this file)
├── sorting/
│   ├── README.md (sorting guide)
│   └── README.md (category guide)
python/algorithms/  (maintained implementations)
tests/algorithms/   (pytest coverage)
├── searching/
├── dp/
├── graphs/
├── string-algorithms/
├── greedy/
├── math/
├── bit-manipulation/
└── geometry/
```

---

## ✅ How to Use

1. **Learn concept:** Read category README (e.g., `sorting/README.md`)
2. **See implementations:** Check the linked file under `python/algorithms/`
3. **Practice problems:** Use the linked tests and the problem lists in `docs/07-patterns/`
4. **Run tests:** `pytest tests/algorithms/test_sorting.py`

---

## 🎯 All Algorithms At a Glance

### Sorting (8 algorithms)
- Bubble, Selection, Insertion, Merge, Quick, Heap, Counting, Radix

### Searching (3 algorithms)
- Linear, Binary, Binary (recursive)

### Dynamic Programming (10+ patterns)
- Fibonacci, Knapsack, LCS, LIS, Edit Distance, Coin Change, Matrix Chain, etc.

### Graph (8+ algorithms)
- BFS, DFS, Topological Sort, Dijkstra, Bellman-Ford, Kruskal, Prim, Floyd-Warshall

### String Matching (4 algorithms)
- KMP, Z-Algorithm, Rabin-Karp, Suffix Arrays

### Other (15+ techniques)
- Greedy, Math, Bit Manipulation, Geometry

**Total:** 50+ algorithms with complete implementations

---

**Last updated:** 2026-05-22
