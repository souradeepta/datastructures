# Interview Algorithms Quick Reference

A single-page reference covering complexity, patterns, trade-offs, and decision rules for every algorithm category tested in FAANG-level SDE interviews.

---

## Master Complexity Cheat Sheet

### Sorting

| Algorithm | Best | Average | Worst | Space | Stable | When to use |
|-----------|------|---------|-------|-------|--------|-------------|
| Bubble | O(n) | O(n²) | O(n²) | O(1) | Yes | Never in practice |
| Selection | O(n²) | O(n²) | O(n²) | O(1) | No | Minimizing swaps |
| Insertion | O(n) | O(n²) | O(n²) | O(1) | Yes | Nearly sorted, small n |
| Merge | O(n log n) | O(n log n) | O(n log n) | O(n) | Yes | Stable sort guarantee |
| Quick | O(n log n) | O(n log n) | O(n²) | O(log n) | No | General purpose, fast constants |
| Heap | O(n log n) | O(n log n) | O(n log n) | O(1) | No | Worst-case guarantee, O(1) space |
| Counting | O(n+k) | O(n+k) | O(n+k) | O(k) | Yes | Integer keys, small range |
| Radix | O(d(n+k)) | O(d(n+k)) | O(d(n+k)) | O(n+k) | Yes | Fixed-length integers/strings |
| Bucket | O(n+k) | O(n+k) | O(n²) | O(n+k) | Yes | Uniform float distribution |
| Tim | O(n) | O(n log n) | O(n log n) | O(n) | Yes | Python/Java stdlib |

### Searching

| Algorithm | Best | Average | Worst | Space | Requirement |
|-----------|------|---------|-------|-------|-------------|
| Linear | O(1) | O(n) | O(n) | O(1) | None |
| Binary | O(1) | O(log n) | O(log n) | O(1) | Sorted |
| Jump | O(1) | O(√n) | O(√n) | O(1) | Sorted |
| Interpolation | O(1) | O(log log n) | O(n) | O(1) | Sorted, uniform |
| Exponential | O(1) | O(log i) | O(log n) | O(1) | Sorted |
| QuickSelect | O(n) | O(n) | O(n²) | O(1) | None |

### Graph

| Algorithm | Time | Space | Use case |
|-----------|------|-------|----------|
| BFS | O(V+E) | O(V) | Shortest path unweighted, level order |
| DFS | O(V+E) | O(V) | Connectivity, cycle detection, SCC |
| Dijkstra | O((V+E) log V) | O(V) | SSSP non-negative weights |
| Bellman-Ford | O(VE) | O(V) | SSSP with negative edges |
| Floyd-Warshall | O(V³) | O(V²) | All-pairs shortest paths |
| Kruskal | O(E log E) | O(V) | MST, sparse graphs |
| Prim | O((V+E) log V) | O(V) | MST, dense graphs |
| Topological Sort | O(V+E) | O(V) | DAG ordering |
| Tarjan SCC | O(V+E) | O(V) | Strongly connected components |
| A* | O(V log V) | O(V) | Heuristic shortest path |

### Dynamic Programming

| Problem | Recurrence | Time | Space | Optimization |
|---------|-----------|------|-------|--------------|
| Fibonacci | dp[i] = dp[i-1] + dp[i-2] | O(n) | O(1) | Variable rolling |
| 0/1 Knapsack | dp[i][w] = max(dp[i-1][w], dp[i-1][w-wi]+vi) | O(nW) | O(W) | 1D array |
| Unbounded Knapsack | dp[w] = max(dp[w], dp[w-wi]+vi) | O(nW) | O(W) | Same array |
| LCS | dp[i][j] = match+dp[i-1][j-1] or max(dp[i-1][j],dp[i][j-1]) | O(mn) | O(min(m,n)) | Row rolling |
| LIS | Binary search on patience sort | O(n log n) | O(n) | Bisect |
| Edit Distance | dp[i][j] = min(ins,del,replace) | O(mn) | O(min(m,n)) | Row rolling |
| Coin Change | dp[i] = min(dp[i-c]+1) | O(n·amount) | O(amount) | None |
| Matrix Chain | dp[i][j] = min_k(dp[i][k]+dp[k+1][j]+cost) | O(n³) | O(n²) | Knuth-Yao |
| Burst Balloons | dp[i][j] = max_k(nums[i-1]*nums[k]*nums[j+1]+...) | O(n³) | O(n²) | None |

### String Algorithms

| Algorithm | Preprocessing | Search | Space | Use case |
|-----------|--------------|--------|-------|----------|
| Naive | O(1) | O(nm) | O(1) | Simple, short pattern |
| KMP | O(m) | O(n) | O(m) | Single pattern |
| Z-Algorithm | O(n+m) | O(1) | O(n+m) | Pattern matching via concatenation |
| Rabin-Karp | O(m) | O(n) avg | O(1) | Rolling hash, multiple patterns |
| Boyer-Moore | O(m+k) | O(n/m) avg | O(k) | Long patterns, large alphabet |
| Aho-Corasick | O(Σ|pi|·k) | O(n+z) | O(Σ|pi|·k) | Multiple pattern matching |
| Suffix Array | O(n log n) | O(m log n) | O(n) | Substring search, LCP queries |
| Manacher | O(n) | — | O(n) | All palindromic substrings |

---

## Algorithm Selection Decision Trees

### "Which sort should I use?"

```mermaid
flowchart TD
    A[Sort needed] --> B{Stability<br/>required?}
    B -->|Yes| C{Space constraint?}
    B -->|No| D{Worst-case O(n log n)<br/>needed?}
    
    C -->|O(n) OK| E{Input type?}
    C -->|O(1) only| F[Counting/Radix<br/>integers only]
    
    E -->|General| G[Merge Sort]
    E -->|Nearly sorted| H[Insertion Sort<br/>O(n) best case]
    E -->|Integers, small k| F
    
    D -->|Yes| I[Heap Sort<br/>O(n log n) guaranteed]
    D -->|No| J{Real-world perf?}
    
    J -->|Best avg perf| K[Quick Sort<br/>random pivot]
    J -->|Python/Java| L[Timsort built-in]
    
    style G fill:#a5d6a7
    style K fill:#64b5f6
    style I fill:#ffd54f
    style F fill:#ffb74d
```

### "Which graph algorithm?"

```mermaid
flowchart TD
    A[Graph Problem] --> B{Shortest path?}
    B -->|Yes| C{Negative edges?}
    B -->|No| D{MST?}
    B -->|No| E{Connectivity?}
    
    C -->|No| F{Single source?}
    C -->|Yes| G{Negative cycle?}
    
    F -->|Yes| H[Dijkstra O((V+E)logV)]
    F -->|No| I[Floyd-Warshall O(V³)]
    
    G -->|Detect| J[Bellman-Ford O(VE)]
    G -->|No cycles| K[Bellman-Ford then Dijkstra]
    
    D -->|Sparse graph| L[Kruskal O(E log E)]
    D -->|Dense graph| M[Prim O((V+E)logV)]
    
    E -->|SCCs| N[Tarjan O(V+E)]
    E -->|Topological order| O[Kahn's BFS O(V+E)]
    E -->|Cut vertices| P[Tarjan Bridges O(V+E)]
    
    style H fill:#a5d6a7
    style I fill:#64b5f6
    style L fill:#ffd54f
```

### "Which DP pattern?"

```mermaid
flowchart TD
    A[DP Problem] --> B{How many<br/>dimensions?}
    B -->|1D| C{Linear recurrence?}
    B -->|2D sequences| D{Two strings?}
    B -->|2D interval| E{Optimal split?}
    
    C -->|Can reuse items| F[Unbounded Knapsack<br/>iterate forward]
    C -->|Each item once| G[0/1 Knapsack<br/>iterate backward]
    C -->|Maximize length| H[LIS O(n log n)]
    C -->|Count ways| I[Coin Change / Fibonacci]
    
    D -->|Match/align| J[LCS / Edit Distance<br/>O(mn)]
    D -->|Palindrome| K[Palindromic Subsequence<br/>O(n²)]
    
    E -->|All splits, minimize cost| L[Matrix Chain / Knuth-Yao<br/>O(n² or n³)]
    E -->|Balloon-type| M[Burst Balloons O(n³)]
    
    style F fill:#a5d6a7
    style J fill:#64b5f6
    style L fill:#ffd54f
```

---

## Pattern Recognition Guide

### When you see these keywords → use this algorithm

| Problem Description | Algorithm | Key Signal |
|--------------------|-----------|-----------|
| "Shortest path", no negative | Dijkstra | Weighted, non-negative |
| "Shortest path", negative weights | Bellman-Ford | Negative edges |
| "All pairs shortest" | Floyd-Warshall | Multiple sources |
| "Minimum spanning tree" | Kruskal/Prim | Connect all nodes |
| "Topological order" | Kahn's BFS or DFS | DAG, prerequisites |
| "Strongly connected" | Tarjan SCC | Directed graph |
| "Max flow" | Dinic's | Capacitated edges |
| "Bipartite matching" | Hopcroft-Karp | Two-set pairing |
| "Find ALL solutions" | Backtracking | Constraint satisfaction |
| "Count ways / min cost" | DP | Optimal substructure |
| "Best of prefix choices" | Greedy | Matroid structure |
| "Count numbers with property" | Digit DP | Bound on value |
| "Subsets, bit tricks" | Bitmask DP | k ≤ 20 |
| "Interval splitting" | Interval DP | dp[i][j] |
| "Tree paths / queries" | Tree DP or HLD | Binary tree / n-ary |
| "Pattern in text" | KMP / Z-algo | Single pattern |
| "Multiple patterns" | Aho-Corasick | Dictionary matching |
| "Palindromes" | Manacher | All substrings O(n) |
| "Convex hull" | Andrew's Monotone Chain | Point set |
| "kth smallest" | QuickSelect | Unsorted array |
| "Range queries, offline" | Mo's Algorithm | Offline, multiple queries |
| "Prefix sums, updates" | Fenwick Tree | Point update, range query |
| "Range queries, updates" | Segment Tree | Range update, range query |

---

## Interview Q&A: High-Frequency Questions

### Q1: Why is QuickSort faster than MergeSort in practice despite both being O(n log n)?

**Answer:**
- **Cache locality**: QuickSort operates in-place with sequential memory access; cache lines stay hot. MergeSort allocates an O(n) auxiliary array and jumps between arrays.
- **Constant factors**: QuickSort's inner loop is extremely tight (compare, swap). MergeSort copies elements on every merge.
- **Recursion overhead**: With median-of-3 pivot, QuickSort's recursion depth is O(log n); with good partitioning, each level touches ~n elements once.
- **Real numbers**: On random data, QuickSort is 2-3× faster than MergeSort despite the same asymptotic complexity.
- **When to prefer MergeSort**: Need stable sort, worst-case guarantee (quicksort is O(n²) adversarial), or sorting linked lists (merge sort avoids random access).

### Q2: Explain the difference between BFS and DFS and when to use each.

**Answer:**

| Property | BFS | DFS |
|----------|-----|-----|
| Data structure | Queue (FIFO) | Stack (recursion or explicit) |
| Order | Level by level | Depth first, then backtrack |
| Memory | O(w) where w = max width | O(h) where h = max depth |
| Shortest path | Yes, unweighted | No |
| Cycle detection | Yes | Yes |
| Topological sort | Yes (Kahn's) | Yes (reverse post-order) |

Use BFS when:
- Need shortest path in unweighted graph
- Finding nodes at a specific distance
- Level-order traversal

Use DFS when:
- Checking connectivity, cycle detection
- Topological sort (reverse post-order)
- Generating all paths (backtracking)
- Tree traversal (preorder/inorder/postorder)

### Q3: When does Dijkstra fail, and what do you use instead?

**Answer:**
Dijkstra fails when **edge weights are negative**. The greedy invariant assumes that once a node is finalized (popped from the heap), its distance is optimal. A later-discovered negative edge could make a path through an "unvisited" node shorter.

```
Example: A → B (weight 5), A → C (weight 2), C → B (weight -4)
Dijkstra finalizes B at distance 5 via A→B.
Correct shortest path: A→C→B = 2 + (-4) = -2.
Dijkstra gives wrong answer.
```

**Alternative: Bellman-Ford** — relaxes ALL edges V-1 times, handles negative edges.
**If negative cycle exists**: Bellman-Ford detects it (distance decreases on Vth pass).
**For dense graphs with negative edges**: Use SPFA (Shortest Path Faster Algorithm), but worst-case is still O(VE).

### Q4: Memoization vs Tabulation — when to use which?

**Answer:**

| | Memoization (top-down) | Tabulation (bottom-up) |
|--|----------------------|----------------------|
| Direction | Recursive, cache results | Iterative, fill table |
| State computation | Only needed states | All states |
| Stack risk | Possible stack overflow | None |
| Space optimization | Hard | Easy (rolling array) |
| Complexity | Same asymptotically | Same asymptotically |
| Implementation | Natural recursion | Explicit loop order |

Use **memoization** when:
- Problem has many states but only a fraction are visited
- Recursion structure maps naturally to the problem
- You're prototyping (easier to write correctly)

Use **tabulation** when:
- All states will be computed anyway
- Need space optimization (rolling arrays)
- Need to avoid stack overflow for large n
- Performance-critical (avoids function call overhead)

### Q5: Explain the two-pointer technique and its variants.

**Answer:**
Two-pointer uses two indices moving through a data structure, usually toward each other or in the same direction.

**Variant 1: Opposite ends (sorted array)**
```python
def two_sum(arr, target):
    l, r = 0, len(arr) - 1
    while l < r:
        s = arr[l] + arr[r]
        if s == target: return (l, r)
        elif s < target: l += 1
        else: r -= 1
```
Use: Two Sum (sorted), Container with Most Water, 3Sum

**Variant 2: Sliding window (same direction)**
```python
def min_window_substring(s, t):
    need = Counter(t)
    have, total = 0, len(need)
    l, res = 0, ""
    for r, c in enumerate(s):
        need[c] -= 1
        if need[c] == 0: have += 1
        while have == total:
            if not res or r-l+1 < len(res):
                res = s[l:r+1]
            need[s[l]] += 1
            if need[s[l]] == 1: have -= 1
            l += 1
    return res
```
Use: Longest substring without repeat, Minimum window substring

**Variant 3: Fast/slow pointers**
```python
def has_cycle(head):
    slow = fast = head
    while fast and fast.next:
        slow, fast = slow.next, fast.next.next
        if slow is fast: return True
    return False
```
Use: Cycle detection, finding cycle start, middle of linked list

### Q6: How do you detect a cycle in a directed graph?

**Answer:**
Use DFS with three states: unvisited (0), in-stack (1), done (2).

```python
def has_cycle_directed(graph, n):
    state = [0] * n  # 0=unvisited, 1=in-stack, 2=done
    
    def dfs(node):
        state[node] = 1  # mark in current path
        for neighbor in graph[node]:
            if state[neighbor] == 1:
                return True   # back edge = cycle
            if state[neighbor] == 0:
                if dfs(neighbor):
                    return True
        state[node] = 2  # done, not in any cycle
        return False
    
    return any(dfs(i) for i in range(n) if state[i] == 0)
```

**Undirected graph**: Use DFS tracking parent, or Union-Find.
```python
def has_cycle_undirected(graph, n):
    parent = list(range(n))
    def find(x):
        while parent[x] != x: parent[x] = parent[parent[x]]; x = parent[x]
        return x
    def union(x, y):
        px, py = find(x), find(y)
        if px == py: return True  # already connected = cycle
        parent[px] = py; return False
    
    for u in range(n):
        for v in graph[u]:
            if u < v and union(u, v): return True
    return False
```

### Q7: Explain Union-Find and its time complexity.

**Answer:**
Union-Find (Disjoint Set Union) tracks which elements are in the same set.

Two optimizations make it nearly O(1) per operation:
1. **Path compression**: During `find`, make every node point directly to root.
2. **Union by rank**: Always attach shorter tree under taller tree.

```python
class UnionFind:
    def __init__(self, n):
        self.parent = list(range(n))
        self.rank = [0] * n
    
    def find(self, x):
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])  # path compression
        return self.parent[x]
    
    def union(self, x, y):
        px, py = self.find(x), self.find(y)
        if px == py: return False
        if self.rank[px] < self.rank[py]: px, py = py, px
        self.parent[py] = px
        if self.rank[px] == self.rank[py]: self.rank[px] += 1
        return True
```

**Time complexity**: O(α(n)) per operation where α is the inverse Ackermann function — effectively constant (≤ 4 for all practical n).

**Use cases**: Kruskal's MST, cycle detection, number of connected components, dynamic connectivity.

### Q8: When do you use a heap vs a sorted array vs a BST?

**Answer:**

| Operation | Heap | Sorted Array | BST (balanced) |
|-----------|------|-------------|---------------|
| Insert | O(log n) | O(n) | O(log n) |
| Delete min/max | O(log n) | O(1) | O(log n) |
| Delete arbitrary | O(n) | O(n) | O(log n) |
| Search | O(n) | O(log n) | O(log n) |
| Find min/max | O(1) | O(1) | O(log n) |
| Rank/Order stats | O(n) | O(1) | O(log n) |

Use **Heap** when: repeatedly need min/max, priority queue semantics (Dijkstra, scheduling), don't need search.
Use **Sorted Array** when: static data, frequent search, need kth element by index.
Use **BST** when: frequent insert/delete AND search, range queries, order statistics.

### Q9: What is the difference between BFS on a graph vs BFS on a tree?

**Answer:**
- **Tree BFS**: No visited set needed (no cycles possible). Each node has exactly one parent.
- **Graph BFS**: Must track visited nodes to avoid infinite loops on cycles.

```python
# Tree BFS (no visited set needed)
def bfs_tree(root):
    queue = deque([root])
    while queue:
        node = queue.popleft()
        process(node)
        for child in node.children:
            queue.append(child)

# Graph BFS (visited set required)
def bfs_graph(start, graph):
    visited = {start}
    queue = deque([start])
    while queue:
        node = queue.popleft()
        process(node)
        for neighbor in graph[node]:
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append(neighbor)
```

Also: In trees, BFS naturally gives level-order traversal. In graphs, "levels" correspond to shortest-path distances from the source.

### Q10: Explain the Sliding Window pattern.

**Answer:**
Sliding window maintains a contiguous subarray/substring satisfying some constraint, expanding or contracting as needed.

**Fixed-size window**: Move window by one each step.
```python
def max_sum_k_elements(arr, k):
    window_sum = sum(arr[:k])
    max_sum = window_sum
    for i in range(k, len(arr)):
        window_sum += arr[i] - arr[i-k]  # add new, remove old
        max_sum = max(max_sum, window_sum)
    return max_sum
```

**Variable-size window**: Expand right, contract left when constraint violated.
```python
def longest_substring_k_distinct(s, k):
    counts = {}
    l = max_len = 0
    for r, c in enumerate(s):
        counts[c] = counts.get(c, 0) + 1
        while len(counts) > k:
            counts[s[l]] -= 1
            if counts[s[l]] == 0: del counts[s[l]]
            l += 1
        max_len = max(max_len, r - l + 1)
    return max_len
```

Key insight: When to shrink the window? When the **window validity condition is violated**.

### Q11: Explain Binary Search on answer space.

**Answer:**
Instead of searching for a value in a sorted array, binary search on the *answer* itself when:
- The answer is monotonic: "is X feasible?" transitions from False→True (or True→False)
- Checking feasibility for a given value X is cheaper than finding the minimum X directly

```python
# Example: "Koko Eating Bananas" - find minimum speed to eat all piles in h hours
def min_eating_speed(piles, h):
    def can_finish(speed):
        return sum((p + speed - 1) // speed for p in piles) <= h
    
    lo, hi = 1, max(piles)
    while lo < hi:
        mid = (lo + hi) // 2
        if can_finish(mid):
            hi = mid      # speed mid works, try smaller
        else:
            lo = mid + 1  # speed mid too slow
    return lo
```

Pattern: Binary search on answer when problem asks "find minimum X such that [condition]" or "find maximum X such that [condition]".

Common problems: Koko Eating Bananas, Ship Packages, Split Array Largest Sum, Find Minimum in Rotated Array.

### Q12: How do you think about space optimization in DP?

**Answer:**
Most 2D DP tables can be reduced to 1D or 2 rows.

**Rule**: If `dp[i][j]` depends only on `dp[i-1][j]` and `dp[i][j-1]`, you only need previous row.

```python
# LCS - Original O(mn) space
def lcs_2d(s1, s2):
    m, n = len(s1), len(s2)
    dp = [[0]*(n+1) for _ in range(m+1)]
    for i in range(1, m+1):
        for j in range(1, n+1):
            if s1[i-1] == s2[j-1]: dp[i][j] = dp[i-1][j-1] + 1
            else: dp[i][j] = max(dp[i-1][j], dp[i][j-1])
    return dp[m][n]

# LCS - O(n) space optimization
def lcs_1d(s1, s2):
    m, n = len(s1), len(s2)
    dp = [0] * (n + 1)
    for i in range(1, m+1):
        prev = 0                    # represents dp[i-1][j-1]
        for j in range(1, n+1):
            temp = dp[j]            # save dp[i-1][j] before overwrite
            if s1[i-1] == s2[j-1]: dp[j] = prev + 1
            else: dp[j] = max(dp[j], dp[j-1])
            prev = temp
    return dp[n]
```

**0/1 Knapsack**: Iterate capacity in **reverse** to avoid using same item twice.
**Unbounded Knapsack**: Iterate capacity **forward** to allow reuse.

---

## Java Implementation Templates

### Binary Search Template

```java
int binarySearch(int[] arr, int target) {
    int lo = 0, hi = arr.length - 1;
    while (lo <= hi) {
        int mid = lo + (hi - lo) / 2;  // avoid overflow
        if (arr[mid] == target) return mid;
        else if (arr[mid] < target) lo = mid + 1;
        else hi = mid - 1;
    }
    return -1;
}

// Find first occurrence of target
int lowerBound(int[] arr, int target) {
    int lo = 0, hi = arr.length;
    while (lo < hi) {
        int mid = lo + (hi - lo) / 2;
        if (arr[mid] < target) lo = mid + 1;
        else hi = mid;
    }
    return lo;  // first index where arr[lo] >= target
}
```

### BFS Template

```java
void bfs(int start, List<List<Integer>> graph) {
    boolean[] visited = new boolean[graph.size()];
    Queue<Integer> queue = new LinkedList<>();
    queue.offer(start);
    visited[start] = true;
    
    while (!queue.isEmpty()) {
        int node = queue.poll();
        process(node);
        for (int neighbor : graph.get(node)) {
            if (!visited[neighbor]) {
                visited[neighbor] = true;
                queue.offer(neighbor);
            }
        }
    }
}
```

### DFS Template (iterative)

```java
void dfs(int start, List<List<Integer>> graph) {
    boolean[] visited = new boolean[graph.size()];
    Deque<Integer> stack = new ArrayDeque<>();
    stack.push(start);
    
    while (!stack.isEmpty()) {
        int node = stack.pop();
        if (visited[node]) continue;
        visited[node] = true;
        process(node);
        for (int neighbor : graph.get(node)) {
            if (!visited[neighbor]) stack.push(neighbor);
        }
    }
}
```

### DP Knapsack Template

```java
// 0/1 Knapsack
int knapsack01(int[] weights, int[] values, int capacity) {
    int n = weights.length;
    int[] dp = new int[capacity + 1];
    for (int i = 0; i < n; i++) {
        for (int w = capacity; w >= weights[i]; w--) {  // reverse!
            dp[w] = Math.max(dp[w], dp[w - weights[i]] + values[i]);
        }
    }
    return dp[capacity];
}

// Unbounded Knapsack
int knapsackUnbounded(int[] weights, int[] values, int capacity) {
    int[] dp = new int[capacity + 1];
    for (int w = 0; w <= capacity; w++) {
        for (int i = 0; i < weights.length; i++) {
            if (weights[i] <= w) {  // forward!
                dp[w] = Math.max(dp[w], dp[w - weights[i]] + values[i]);
            }
        }
    }
    return dp[capacity];
}
```

### Union-Find Template

```java
class UnionFind {
    int[] parent, rank;
    int components;
    
    UnionFind(int n) {
        parent = new int[n]; rank = new int[n]; components = n;
        for (int i = 0; i < n; i++) parent[i] = i;
    }
    
    int find(int x) {
        if (parent[x] != x) parent[x] = find(parent[x]);
        return parent[x];
    }
    
    boolean union(int x, int y) {
        int px = find(x), py = find(y);
        if (px == py) return false;
        if (rank[px] < rank[py]) { int t = px; px = py; py = t; }
        parent[py] = px;
        if (rank[px] == rank[py]) rank[px]++;
        components--;
        return true;
    }
}
```

---

## Common Pitfalls and How to Avoid Them

| Pitfall | Example | Fix |
|---------|---------|-----|
| Integer overflow | `mid = (lo+hi)/2` | Use `lo + (hi-lo)/2` |
| Off-by-one in binary search | Using `<=` vs `<` | Use `lo < hi` for exclusive upper bound template |
| Modifying graph while iterating | DFS edge removal | Collect edges first, then remove |
| Forgetting visited set in graph | Infinite BFS loop | Always use visited before enqueuing |
| Wrong knapsack loop order | 0/1 vs unbounded | Reverse = 0/1, Forward = unbounded |
| Not copying path in backtracking | `result.append(path)` | Use `result.append(path[:])` |
| Stack overflow in deep DFS | n=10⁶ recursive DFS | Convert to iterative |
| Wrong base case in DP | dp[0] = 1 vs 0 | Trace first 2-3 cases manually |
| Missing return in recursive DP | Returns None | Ensure all paths return value |
| Comparing floats in geometry | `cross_product == 0` | Use `abs(cross_product) < EPS` |

---

## Time Complexity Rules of Thumb

| n | Acceptable Complexity | Algorithm Family |
|---|----------------------|-----------------|
| n ≤ 10 | O(n!) | Permutations, brute force |
| n ≤ 20 | O(2ⁿ) | Bitmask DP |
| n ≤ 100 | O(n³) | Floyd-Warshall, interval DP |
| n ≤ 1000 | O(n²) | Two nested loops, O(n²) DP |
| n ≤ 10⁵ | O(n log n) | Sorting, divide-conquer, heap |
| n ≤ 10⁶ | O(n) | Linear scan, hash map |
| n ≤ 10⁸ | O(log n) or O(√n) | Binary search, sieve |

---

## Guide Links

| Topic | Guide |
|-------|-------|
| Sorting algorithms | [sorting/sorting.md](sorting/sorting.md) |
| Searching algorithms | [searching/searching.md](searching/searching.md) |
| Dynamic programming fundamentals | [dp/dp_fundamentals.md](dp/dp_fundamentals.md) |
| DP: string patterns | [dp/dp_strings.md](dp/dp_strings.md) |
| DP: interval & advanced | [dp/dp_interval_advanced.md](dp/dp_interval_advanced.md) |
| Backtracking patterns | [dp/backtracking_patterns.md](dp/backtracking_patterns.md) |
| Grid DP patterns | [dp/grid_dp_patterns.md](dp/grid_dp_patterns.md) |
| Graph algorithms | [graph/graph_algorithms.md](graph/graph_algorithms.md) |
| Graph traversal patterns | [graph/traversal_patterns.md](graph/traversal_patterns.md) |
| Tree DP guide | [graph/tree_dp_guide.md](graph/tree_dp_guide.md) |
| String algorithms | [string/string_algorithms.md](string/string_algorithms.md) |
| Math algorithms | [math/math_algorithms.md](math/math_algorithms.md) |
| Advanced algorithms (index) | [advanced/advanced_algorithms.md](advanced/advanced_algorithms.md) |
| DP optimization (CHT, SOS) | [advanced/dp_optimization.md](advanced/dp_optimization.md) |
| Graph flow & matching | [advanced/graph_flow_matching.md](advanced/graph_flow_matching.md) |
| String advanced (suffix array) | [advanced/string_advanced.md](advanced/string_advanced.md) |
| Computational geometry | Planned |
| Advanced data structures | [Data Structures overview](../06-data-structures/README.md) |
