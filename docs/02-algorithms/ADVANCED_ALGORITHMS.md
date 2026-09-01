# Advanced Algorithms Implementation Guide

A deep-dive reference into 30+ advanced algorithms for senior SDE interviews. Each section includes the core idea, implementation in Python and Java, step-by-step trace, complexity analysis, and interview Q&A.

---

## Navigation

| Category | Algorithms | Guide |
|----------|-----------|-------|
| DP Optimization | CHT, Knuth-Yao, SOS, Digit DP | [advanced/dp_optimization.md](advanced/dp_optimization.md) |
| Graph Flow & Matching | Dinic's, Min Cost Flow, Hopcroft-Karp, 2-SAT | [advanced/graph_flow_matching.md](advanced/graph_flow_matching.md) |
| String Advanced | Suffix Array, Aho-Corasick, Manacher, Z-algo | [advanced/string_advanced.md](advanced/string_advanced.md) |
| Computational Geometry | Convex Hull, Closest Pair, Sweep Line | Planned |
| Advanced Data Structures | HLD, Segment Tree, Mo's, Sqrt Decomp | [Data Structures overview](../06-data-structures/README.md) |

---

## Master Algorithm Selection

```mermaid
flowchart TD
    Start([Problem Type?]) --> DP{DP?}
    Start --> Graph{Graph?}
    Start --> String{String?}
    Start --> Geo{Geometry?}
    Start --> DS{Data Structure?}

    DP --> DPOpt{Optimize<br/>recurrence?}
    DPOpt -->|Linear cost| CHT[Convex Hull Trick]
    DPOpt -->|Interval, quad ineq| KY[Knuth-Yao O(n²)]
    DPOpt -->|Subsets| SOS[SOS DP O(k·2^k)]
    DPOpt -->|Digit constraints| Digit[Digit DP]
    DPOpt -->|Tree structure| TreeDP[Tree DP O(n)]

    Graph --> Flow{Flow?}
    Flow -->|Max flow| Dinic[Dinic's O(V²E)]
    Flow -->|Min cost| MCMF[Min Cost Max Flow]
    Flow -->|Bipartite| HK[Hopcroft-Karp O(E√V)]
    Graph --> Sat{Satisfiability?}
    Sat --> TwoSAT[2-SAT via SCC]
    Graph --> Cut{Cuts?}
    Cut --> AP[Articulation Points + Bridges]

    String --> Pat{Pattern?}
    Pat -->|Multi-pattern| AC[Aho-Corasick]
    Pat -->|Suffix queries| SA[Suffix Array + LCP]
    Pat -->|Palindromes| Man[Manacher O(n)]
    Pat -->|Prefix match| ZAlgo[Z-Algorithm]

    Geo --> Hull[Convex Hull O(n log n)]
    Geo --> CP[Closest Pair O(n log n)]
    Geo --> Inter[Line Intersection O(1)]

    DS --> Range{Range queries?}
    Range -->|Tree paths| HLD[Heavy-Light Decomp]
    Range -->|Offline queries| Mo[Mo's Algorithm]
    Range -->|Block queries| Sqrt[Sqrt Decomposition]
```

---

## Algorithm 1: Convex Hull Trick (CHT)

### Core Idea
Transform O(n²) DP where `dp[i] = min_j(f(j) + g(j)*i)` into O(n) or O(n log n) by maintaining a lower convex hull of linear functions.

### When to Apply
The recurrence must have the form `dp[i] = min over j<i of { a[j]*x[i] + b[j] }` where `a[j]` are slopes.

### Step-by-Step Trace

```
Problem: dp[i] = min_j<i(dp[j] + (a[i]-a[j])² )
         = dp[j] + a[i]² - 2*a[i]*a[j] + a[j]²
         = (-2*a[j]) * a[i] + (dp[j] + a[j]²) + a[i]²
         
For each j, this is a line: y = m*x + b where m = -2*a[j], b = dp[j]+a[j]², x = a[i]

Lines: j=0: y = 0*x + 0       (m=0, b=0)
       j=1: y = -4*x + 5      (m=-4, b=5) if a=[0,2,...], dp=[0,...]
       j=2: y = -6*x + 10     (m=-6, b=10) if a=[0,2,3,...]

For query x=a[i], find line with minimum y.
Convex hull: maintain lines sorted by slope.
For monotone queries: use pointer advancing in O(1).
```

### Python Implementation

```python
from collections import deque

class ConvexHullTrick:
    """Minimum convex hull trick with monotone queries."""
    
    def __init__(self):
        self.hull = deque()  # deque of (slope, intercept) lines
    
    def _bad(self, l1, l2, l3):
        """True if l2 is never minimum (l3 dominates l2 given l1)."""
        # Intersection of l1,l3 is to left of intersection of l1,l2
        # l1: y=m1*x+b1, l2: y=m2*x+b2, l3: y=m3*x+b3
        m1,b1 = l1; m2,b2 = l2; m3,b3 = l3
        return (b3-b1)*(m1-m2) <= (b2-b1)*(m1-m3)
    
    def add_line(self, m, b):
        """Add line y = m*x + b. Lines must be added in decreasing slope order."""
        new_line = (m, b)
        while len(self.hull) >= 2 and self._bad(self.hull[-2], self.hull[-1], new_line):
            self.hull.pop()
        self.hull.append(new_line)
    
    def query_min(self, x):
        """Query minimum y at x. Queries must be in increasing x order."""
        while len(self.hull) >= 2:
            m1,b1 = self.hull[0]; m2,b2 = self.hull[1]
            if m1*x + b1 >= m2*x + b2:
                self.hull.popleft()
            else:
                break
        m, b = self.hull[0]
        return m * x + b

def cht_example():
    """
    Problem: Minimum cost to group n tasks into segments.
    dp[i] = min over j<i of (dp[j] + cost(j+1..i))
    where cost(l,r) = (sum[l..r])^2
    """
    a = [0, 3, 1, 4, 2]   # task weights
    prefix = [0] * (len(a) + 1)
    for i, x in enumerate(a):
        prefix[i+1] = prefix[i] + x
    
    n = len(a)
    dp = [float('inf')] * (n + 1)
    dp[0] = 0
    cht = ConvexHullTrick()
    
    # dp[i] = min_j<i (dp[j] + (prefix[i] - prefix[j])^2)
    # = min_j<i (dp[j] + prefix[i]^2 - 2*prefix[i]*prefix[j] + prefix[j]^2)
    # Line for j: slope = -2*prefix[j], intercept = dp[j] + prefix[j]^2
    # Query at x = prefix[i], add constant prefix[i]^2
    
    cht.add_line(-2*prefix[0], dp[0] + prefix[0]**2)
    for i in range(1, n + 1):
        dp[i] = cht.query_min(prefix[i]) + prefix[i]**2
        cht.add_line(-2*prefix[i], dp[i] + prefix[i]**2)
    
    return dp[n]

print(cht_example())  # Minimum cost
```

### Java Implementation

```java
import java.util.*;

public class ConvexHullTrick {
    private Deque<long[]> hull = new ArrayDeque<>();  // {slope, intercept}
    
    private boolean bad(long[] l1, long[] l2, long[] l3) {
        // l2 is never minimum if l3 intersects before l2 given l1
        return (l3[1] - l1[1]) * (l1[0] - l2[0]) <= (l2[1] - l1[1]) * (l1[0] - l3[0]);
    }
    
    public void addLine(long m, long b) {
        long[] newLine = {m, b};
        while (hull.size() >= 2) {
            long[] last = hull.peekLast();
            long[] secondLast = ((ArrayDeque<long[]>)hull).toArray(new long[0][])[hull.size()-2];
            if (bad(secondLast, last, newLine)) hull.pollLast();
            else break;
        }
        hull.addLast(newLine);
    }
    
    public long queryMin(long x) {
        while (hull.size() >= 2) {
            long[] first = hull.peekFirst();
            long[] second = hull.toArray(new long[0][])[1];
            if (first[0]*x + first[1] >= second[0]*x + second[1])
                hull.pollFirst();
            else break;
        }
        long[] line = hull.peekFirst();
        return line[0] * x + line[1];
    }
    
    // Time: O(n) with monotone queries
    // Space: O(n) for hull
}
```

### Complexity

| Variant | Time | Space |
|---------|------|-------|
| Offline (monotone queries) | O(n) | O(n) |
| Online (arbitrary queries) | O(n log n) | O(n) |
| Li-Chao tree (online) | O(n log C) | O(n log C) |

---

## Algorithm 2: Suffix Array

### Core Idea
A sorted array of all suffixes of a string. Enables O(m log n) pattern search and O(n) LCP queries — more space-efficient than suffix trees.

### Construction Trace

```
String: "banana$"  ($ = sentinel, lexicographically smallest)

All suffixes sorted:
  0: banana$
  1: anana$
  2: nana$
  3: ana$
  4: na$
  5: a$
  6: $

Sorted lexicographically:
  6: $           → rank 0
  5: a$          → rank 1
  3: ana$        → rank 2
  1: anana$      → rank 3
  0: banana$     → rank 4
  4: na$         → rank 5
  2: nana$       → rank 6

SA = [6, 5, 3, 1, 0, 4, 2]

LCP array (longest common prefix between adjacent suffixes in SA):
  LCP[0] = 0  ($, a$ share 0)
  LCP[1] = 1  (a$, ana$ share "a")
  LCP[2] = 3  (ana$, anana$ share "ana")
  LCP[3] = 0  (anana$, banana$ share 0)
  LCP[4] = 0  (banana$, na$ share 0)
  LCP[5] = 2  (na$, nana$ share "na")

LCP = [0, 1, 3, 0, 0, 2]
```

### Python Implementation

```python
def build_suffix_array(s):
    """O(n log² n) suffix array construction."""
    n = len(s)
    sa = sorted(range(n), key=lambda i: s[i:])
    
    # Refine with doubling (O(n log² n))
    rank = [0] * n
    for i, idx in enumerate(sa):
        rank[idx] = i
    
    k = 1
    while k < n:
        def key(i):
            r1 = rank[i]
            r2 = rank[i + k] if i + k < n else -1
            return (r1, r2)
        
        sa = sorted(range(n), key=key)
        new_rank = [0] * n
        new_rank[sa[0]] = 0
        for i in range(1, n):
            if key(sa[i]) != key(sa[i-1]):
                new_rank[sa[i]] = new_rank[sa[i-1]] + 1
            else:
                new_rank[sa[i]] = new_rank[sa[i-1]]
        rank = new_rank
        if rank[sa[-1]] == n - 1:
            break  # all ranks distinct, done
        k *= 2
    
    return sa

def build_lcp(s, sa):
    """Kasai's O(n) LCP array construction."""
    n = len(s)
    rank = [0] * n
    for i, idx in enumerate(sa):
        rank[idx] = i
    
    lcp = [0] * n
    h = 0
    for i in range(n):
        if rank[i] > 0:
            j = sa[rank[i] - 1]
            while i + h < n and j + h < n and s[i+h] == s[j+h]:
                h += 1
            lcp[rank[i]] = h
            if h > 0:
                h -= 1
    return lcp

def search_pattern(s, sa, pattern):
    """Binary search for pattern in suffix array. O(m log n)."""
    n, m = len(s), len(pattern)
    
    # Find leftmost position
    lo, hi = 0, n
    while lo < hi:
        mid = (lo + hi) // 2
        if s[sa[mid]:sa[mid]+m] < pattern:
            lo = mid + 1
        else:
            hi = mid
    left = lo
    
    # Find rightmost position
    hi = n
    while lo < hi:
        mid = (lo + hi) // 2
        if s[sa[mid]:sa[mid]+m] > pattern:
            hi = mid
        else:
            lo = mid + 1
    right = lo
    
    return sa[left:right]  # all starting positions of pattern in s

# Demo
s = "banana$"
sa = build_suffix_array(s)
lcp = build_lcp(s, sa)
print("SA:", sa)     # [6, 5, 3, 1, 0, 4, 2]
print("LCP:", lcp)   # [0, 1, 3, 0, 0, 2, ...]
positions = search_pattern(s, sa, "an")
print("Pattern 'an' at positions:", positions)  # [1, 3]
```

### Java Implementation

```java
public class SuffixArray {
    int[] sa, rank, lcp;
    String s;
    int n;
    
    SuffixArray(String s) {
        this.s = s + "$";
        this.n = this.s.length();
        buildSA();
        buildLCP();
    }
    
    void buildSA() {
        sa = new int[n];
        rank = new int[n];
        int[] tmp = new int[n];
        
        for (int i = 0; i < n; i++) { sa[i] = i; rank[i] = s.charAt(i); }
        
        for (int k = 1; k < n; k <<= 1) {
            final int kk = k;
            final int[] r = rank.clone();
            java.util.Arrays.sort(sa, (a, b) -> {
                if (r[a] != r[b]) return r[a] - r[b];
                int ra = a+kk < n ? r[a+kk] : -1;
                int rb = b+kk < n ? r[b+kk] : -1;
                return ra - rb;
            });
            tmp[sa[0]] = 0;
            for (int i = 1; i < n; i++) {
                tmp[sa[i]] = tmp[sa[i-1]];
                int ra = sa[i-1]+kk < n ? r[sa[i-1]+kk] : -1;
                int rb = sa[i]+kk < n ? r[sa[i]+kk] : -1;
                if (r[sa[i]] != r[sa[i-1]] || ra != rb) tmp[sa[i]]++;
            }
            rank = tmp.clone();
        }
    }
    
    void buildLCP() {  // Kasai's algorithm
        lcp = new int[n];
        int[] inv = new int[n];
        for (int i = 0; i < n; i++) inv[sa[i]] = i;
        int h = 0;
        for (int i = 0; i < n; i++) {
            if (inv[i] > 0) {
                int j = sa[inv[i] - 1];
                while (i+h < n && j+h < n && s.charAt(i+h) == s.charAt(j+h)) h++;
                lcp[inv[i]] = h;
                if (h > 0) h--;
            }
        }
    }
    
    List<Integer> search(String pattern) {
        int m = pattern.length();
        int lo = 0, hi = n;
        while (lo < hi) {
            int mid = (lo+hi)/2;
            if (s.substring(sa[mid], Math.min(sa[mid]+m, n)).compareTo(pattern) < 0) lo = mid+1;
            else hi = mid;
        }
        int left = lo;
        hi = n;
        while (lo < hi) {
            int mid = (lo+hi)/2;
            if (s.substring(sa[mid], Math.min(sa[mid]+m, n)).compareTo(pattern) > 0) hi = mid;
            else lo = mid+1;
        }
        List<Integer> result = new ArrayList<>();
        for (int i = left; i < lo; i++) result.add(sa[i]);
        return result;
    }
}
```

### Complexity

| Operation | Time | Space |
|-----------|------|-------|
| Build SA (naive sort) | O(n log² n) | O(n) |
| Build SA (SA-IS) | O(n) | O(n) |
| Build LCP (Kasai) | O(n) | O(n) |
| Pattern search | O(m log n) | O(1) |
| All occurrences | O(m log n + k) | O(k) |

---

## Algorithm 3: Dinic's Max Flow

### Core Idea
Level graph + blocking flow. The key insight: maintain a BFS level graph and find blocking flows iteratively. Achieves O(V²E) for general graphs, O(E√V) for unit-capacity.

### Step-by-Step Trace

```
Graph: s=0, t=5
Edges: (0→1, cap=10), (0→2, cap=10), (1→2, cap=2), (1→3, cap=4),
       (2→4, cap=9), (3→5, cap=10), (4→3, cap=6), (4→5, cap=10)

Iteration 1:
  BFS from s: level[0]=0, level[1]=1, level[2]=1, level[3]=2, level[4]=2, level[5]=3
  Level graph (only edges going to next level):
    0→1(10), 0→2(10), 1→3(4), 2→4(9), 3→5(10), 4→5(10)
  Find blocking flow using DFS with pointer advancement:
    Path 0→1→3→5: min cap = min(10,4,10)=4, send 4
    Path 0→2→4→5: min cap = min(10,9,10)=9, send 9
    Path 0→1→?→5: 1→3 saturated. Advance pointer.
    DFS stuck, total blocking flow = 13

  Total flow so far: 13

Iteration 2:
  BFS: level[5]=5 (longer path now)
  ...continue until no augmenting path found

Answer: max flow = 19
```

### Python Implementation

```python
from collections import defaultdict, deque

class Dinic:
    def __init__(self, n):
        self.n = n
        self.graph = defaultdict(list)
    
    def add_edge(self, u, v, cap):
        """Add directed edge u→v with given capacity."""
        # graph[u] stores (to, capacity, index into graph[to] for reverse)
        self.graph[u].append([v, cap, len(self.graph[v])])
        self.graph[v].append([u, 0, len(self.graph[u])-1])   # reverse edge, 0 cap
    
    def _bfs(self, s, t, level):
        """Build level graph via BFS. Returns True if t is reachable."""
        level[:] = [-1] * self.n
        level[s] = 0
        q = deque([s])
        while q:
            u = q.popleft()
            for v, cap, _ in self.graph[u]:
                if cap > 0 and level[v] < 0:
                    level[v] = level[u] + 1
                    q.append(v)
        return level[t] >= 0
    
    def _dfs(self, u, t, pushed, level, iter_):
        """Find blocking flow using pointer advancement."""
        if u == t:
            return pushed
        while iter_[u] < len(self.graph[u]):
            v, cap, rev = self.graph[u][iter_[u]]
            if cap > 0 and level[v] == level[u] + 1:
                d = self._dfs(v, t, min(pushed, cap), level, iter_)
                if d > 0:
                    self.graph[u][iter_[u]][1] -= d
                    self.graph[v][rev][1] += d
                    return d
            iter_[u] += 1
        return 0
    
    def max_flow(self, s, t):
        flow = 0
        level = [-1] * self.n
        while self._bfs(s, t, level):
            iter_ = [0] * self.n
            while True:
                f = self._dfs(s, t, float('inf'), level, iter_)
                if f == 0:
                    break
                flow += f
        return flow

# Demo
g = Dinic(6)
g.add_edge(0, 1, 16)
g.add_edge(0, 2, 13)
g.add_edge(1, 2, 10)
g.add_edge(1, 3, 12)
g.add_edge(2, 4, 14)
g.add_edge(3, 2, 9)
g.add_edge(3, 5, 20)
g.add_edge(4, 3, 7)
g.add_edge(4, 5, 4)
print(g.max_flow(0, 5))  # 23
```

### Java Implementation

```java
import java.util.*;

public class Dinic {
    static final int INF = Integer.MAX_VALUE / 2;
    int n;
    List<int[]>[] graph;  // {to, cap, rev}
    int[] level, iter;
    
    @SuppressWarnings("unchecked")
    Dinic(int n) {
        this.n = n;
        graph = new List[n];
        for (int i = 0; i < n; i++) graph[i] = new ArrayList<>();
    }
    
    void addEdge(int u, int v, int cap) {
        graph[u].add(new int[]{v, cap, graph[v].size()});
        graph[v].add(new int[]{u, 0, graph[u].size()-1});
    }
    
    boolean bfs(int s, int t) {
        level = new int[n]; Arrays.fill(level, -1);
        Queue<Integer> q = new LinkedList<>();
        level[s] = 0; q.offer(s);
        while (!q.isEmpty()) {
            int u = q.poll();
            for (int[] e : graph[u]) {
                if (e[1] > 0 && level[e[0]] < 0) {
                    level[e[0]] = level[u] + 1;
                    q.offer(e[0]);
                }
            }
        }
        return level[t] >= 0;
    }
    
    int dfs(int u, int t, int f) {
        if (u == t) return f;
        for (; iter[u] < graph[u].size(); iter[u]++) {
            int[] e = graph[u].get(iter[u]);
            if (e[1] > 0 && level[e[0]] == level[u]+1) {
                int d = dfs(e[0], t, Math.min(f, e[1]));
                if (d > 0) { e[1] -= d; graph[e[0]].get(e[2])[1] += d; return d; }
            }
        }
        return 0;
    }
    
    int maxFlow(int s, int t) {
        int flow = 0;
        while (bfs(s, t)) {
            iter = new int[n];
            int f;
            while ((f = dfs(s, t, INF)) > 0) flow += f;
        }
        return flow;
    }
}
```

### Complexity

| Graph Type | Time |
|-----------|------|
| General | O(V²E) |
| Unit capacity | O(E√V) |
| Bipartite matching | O(E√V) |

---

## Algorithm 4: Aho-Corasick

### Core Idea
Build a trie of all patterns, then add failure links (like KMP) to enable simultaneous matching of all patterns in O(n + total_pattern_length + number_of_matches).

### Construction Trace

```
Patterns: ["he", "she", "his", "hers"]

Trie:
  root
  ├── h → e → (OUTPUT: "he")
  │         └── r → s → (OUTPUT: "hers")
  ├── s → h → e → (OUTPUT: "she")
  └── h → i → s → (OUTPUT: "his")

After building trie, add failure links via BFS:
  root: fail=root
  'h' node: fail=root
  's' node: fail=root
  'h→e' node: fail='e' (no 'e' child of root, fail=root) → fail=root
  's→h' node: fail='h' node
  's→h→e' node: fail='h→e' node, and 'h→e' outputs "he", so 'she' also outputs "he"

Output function (string match when reaching node):
  "she" node outputs: ["she", "he"]

Search "ushers":
  u: no transition, stay root
  s: go to 's' node
  h: go to 's→h' node
  e: go to 's→h→e' node → MATCH "she", follow output link → MATCH "he"
  r: go to 's→h→e→r' = 'h→e→r' node (via fail link)
  s: go to 'h→e→r→s' node → MATCH "hers"

Matches: "she" at 4, "he" at 4, "hers" at 5
```

### Python Implementation

```python
from collections import deque, defaultdict

class AhoCorasick:
    def __init__(self):
        self.goto = [defaultdict(int)]  # goto[state][char] = next_state
        self.fail = [0]
        self.output = [[]]
        self.size = 1  # root = state 0
    
    def _new_state(self):
        self.goto.append(defaultdict(int))
        self.fail.append(0)
        self.output.append([])
        self.size += 1
        return self.size - 1
    
    def add_pattern(self, pattern, pattern_id=None):
        """Insert pattern into trie."""
        state = 0
        for char in pattern:
            if char not in self.goto[state] or self.goto[state][char] == 0:
                next_state = self._new_state()
                self.goto[state][char] = next_state
            state = self.goto[state][char]
        self.output[state].append(pattern if pattern_id is None else pattern_id)
    
    def build(self):
        """Build failure links via BFS."""
        q = deque()
        # Initialize: all depth-1 states have fail link to root
        for char, state in self.goto[0].items():
            if state != 0:
                self.fail[state] = 0
                q.append(state)
        
        while q:
            r = q.popleft()
            for char, s in self.goto[r].items():
                if s == 0:
                    continue
                q.append(s)
                # Find longest proper suffix of r's string that is prefix of some pattern
                state = self.fail[r]
                while state != 0 and char not in self.goto[state]:
                    state = self.fail[state]
                self.fail[s] = self.goto[state].get(char, 0)
                if self.fail[s] == s:
                    self.fail[s] = 0
                # Merge output from fail state
                self.output[s] = self.output[s] + self.output[self.fail[s]]
    
    def search(self, text):
        """Find all pattern occurrences in text. O(n + z)."""
        state = 0
        results = []
        for i, char in enumerate(text):
            # Follow fail links until goto[state][char] exists
            while state != 0 and char not in self.goto[state]:
                state = self.fail[state]
            state = self.goto[state].get(char, 0)
            # Collect outputs (all patterns ending at position i)
            for pattern in self.output[state]:
                results.append((i - len(pattern) + 1, i, pattern))
        return results

# Demo
ac = AhoCorasick()
patterns = ["he", "she", "his", "hers"]
for p in patterns:
    ac.add_pattern(p)
ac.build()

text = "ushers"
matches = ac.search(text)
for start, end, pat in sorted(matches):
    print(f"'{pat}' found at [{start},{end}]")
# Output:
# 'she' found at [1,3]
# 'he' found at [2,3]
# 'hers' found at [2,5]
```

### Java Implementation

```java
import java.util.*;

public class AhoCorasick {
    int[][] go;       // goto table
    int[] fail;       // failure links
    List<String>[] output;
    int size, maxStates;
    
    @SuppressWarnings("unchecked")
    AhoCorasick(int maxPatternLength, int numPatterns) {
        maxStates = maxPatternLength * numPatterns + 1;
        go = new int[maxStates][26];
        fail = new int[maxStates];
        output = new List[maxStates];
        for (int i = 0; i < maxStates; i++) {
            Arrays.fill(go[i], -1);
            output[i] = new ArrayList<>();
        }
        size = 1;
    }
    
    void addPattern(String pattern) {
        int state = 0;
        for (char c : pattern.toCharArray()) {
            int idx = c - 'a';
            if (go[state][idx] == -1) go[state][idx] = size++;
            state = go[state][idx];
        }
        output[state].add(pattern);
    }
    
    void build() {
        Queue<Integer> q = new LinkedList<>();
        for (int c = 0; c < 26; c++) {
            if (go[0][c] == -1) go[0][c] = 0;
            else { fail[go[0][c]] = 0; q.offer(go[0][c]); }
        }
        while (!q.isEmpty()) {
            int u = q.poll();
            output[u].addAll(output[fail[u]]);
            for (int c = 0; c < 26; c++) {
                if (go[u][c] == -1)
                    go[u][c] = go[fail[u]][c];
                else {
                    fail[go[u][c]] = go[fail[u]][c];
                    q.offer(go[u][c]);
                }
            }
        }
    }
    
    List<int[]> search(String text) {
        List<int[]> result = new ArrayList<>();
        int state = 0;
        for (int i = 0; i < text.length(); i++) {
            state = go[state][text.charAt(i) - 'a'];
            for (String pat : output[state])
                result.add(new int[]{i - pat.length() + 1, i});
        }
        return result;
    }
}
```

### Complexity

| Operation | Time | Space |
|-----------|------|-------|
| Build trie | O(Σ\|pi\|) | O(Σ\|pi\| × k) |
| Build fail links | O(Σ\|pi\| × k) | — |
| Search | O(n + z) | O(1) |
| Total | O(Σ\|pi\| × k + n + z) | O(Σ\|pi\| × k) |

k = alphabet size, n = text length, z = number of matches

---

## Algorithm 5: Heavy-Light Decomposition (HLD)

### Core Idea
Decompose a tree into chains where each chain has contiguous segment tree indices. Path queries between any two nodes break into O(log n) chain segments, each answerable in O(log n) via segment tree → O(log² n) per path query.

### Decomposition Trace

```
Tree:
         1
        /|\
       2  3  4
      /|     |
     5  6    7
          |
          8

Heavy child of each node (largest subtree):
  Node 1: children {2(size=5), 3(size=1), 4(size=2)} → heavy=2
  Node 2: children {5(size=1), 6(size=2)} → heavy=6
  Node 4: children {7(size=1)} → heavy=7
  Node 6: children {8(size=1)} → heavy=8

Heavy chains:
  Chain 1: 1 → 2 → 6 → 8 (positions 0,1,2,3)
  Chain 2: 4 → 7            (positions 4,5)
  Chain 3: 3                (position 6)
  Chain 4: 5                (position 7)

Query "sum of values on path 5 → 7":
  Path: 5 → 2 → 1 → 4 → 7
  
  5 is on chain {5} at position 7
  7 is on chain {4,7} at position 5
  
  LCA = 1
  
  Process from 5 upward:
    5's chain head = 5, LCA's chain head = 1
    5's chain head > 1's chain, go up: query segment[7..7], move to parent of 5 = 2
    2's chain head = 1, same as LCA's chain head: stop and query 1..2 (positions of 1 and 2)
  
  Process from 7 upward:
    7's chain head = 4, LCA's chain head = 1
    query segment[4..5], move to parent of 4 = 1
    1's chain head = 1 = LCA chain head: query position of 1 (position 0)
  
  Total: sum of positions {7} + {0,1} + {4,5} + {0} (with dedup on LCA)
```

### Python Implementation

```python
class HLD:
    def __init__(self, n, adj, values):
        self.n = n
        self.adj = adj
        self.values = values
        self.parent = [-1] * (n + 1)
        self.depth = [0] * (n + 1)
        self.heavy = [-1] * (n + 1)   # heavy child
        self.size = [1] * (n + 1)
        self.head = [0] * (n + 1)     # chain head
        self.pos = [0] * (n + 1)      # position in segment tree
        self.segment = [0] * (4 * n)  # segment tree
        self.cur_pos = [0]
        
        self._dfs1(1, -1, 0)
        self._dfs2(1, 1)
        self._build(1, 0, n - 1)
    
    def _dfs1(self, v, p, d):
        """Compute size, heavy child, parent, depth."""
        self.parent[v] = p
        self.depth[v] = d
        max_size = 0
        for u in self.adj[v]:
            if u != p:
                self._dfs1(u, v, d + 1)
                self.size[v] += self.size[u]
                if self.size[u] > max_size:
                    max_size = self.size[u]
                    self.heavy[v] = u
    
    def _dfs2(self, v, h):
        """Assign positions and chain heads."""
        self.head[v] = h
        self.pos[v] = self.cur_pos[0]
        self.cur_pos[0] += 1
        # First process heavy child (keeps chain contiguous)
        if self.heavy[v] != -1:
            self._dfs2(self.heavy[v], h)
        for u in self.adj[v]:
            if u != self.parent[v] and u != self.heavy[v]:
                self._dfs2(u, u)  # new chain
    
    def _build(self, node, start, end):
        """Build segment tree on HLD positions."""
        if start == end:
            # Map position back to original node value
            self.segment[node] = self.values[start]
            return
        mid = (start + end) // 2
        self._build(2*node, start, mid)
        self._build(2*node+1, mid+1, end)
        self.segment[node] = self.segment[2*node] + self.segment[2*node+1]
    
    def _query(self, node, start, end, l, r):
        """Range sum query on segment tree."""
        if r < start or end < l:
            return 0
        if l <= start and end <= r:
            return self.segment[node]
        mid = (start + end) // 2
        return (self._query(2*node, start, mid, l, r) +
                self._query(2*node+1, mid+1, end, l, r))
    
    def path_query(self, u, v):
        """Sum of values on path u→v. O(log² n)."""
        result = 0
        while self.head[u] != self.head[v]:
            if self.depth[self.head[u]] < self.depth[self.head[v]]:
                u, v = v, u
            # u's chain head is deeper, query from head[u] to u
            result += self._query(1, 0, self.n-1, self.pos[self.head[u]], self.pos[u])
            u = self.parent[self.head[u]]
        # Same chain, query from min to max position
        if self.depth[u] > self.depth[v]:
            u, v = v, u
        result += self._query(1, 0, self.n-1, self.pos[u], self.pos[v])
        return result
```

### Complexity

| Operation | Time | Space |
|-----------|------|-------|
| Build | O(n) | O(n) |
| Path query | O(log² n) | O(1) |
| Path update | O(log² n) | O(1) |
| Subtree query | O(log n) | O(1) |

---

## Interview Q&A: Advanced Algorithm Questions

### Q1: When would you choose Suffix Array over Suffix Tree?

**Answer:**
- **Suffix Array** is preferred in practice:
  - Simpler to implement (especially SA-IS for O(n) construction)
  - Better cache performance (contiguous array vs pointer-based tree)
  - Less memory overhead (O(n) vs O(n) but smaller constants)
  - LCP array gives same power as suffix tree for most queries

- **Suffix Tree** advantages:
  - O(m) exact pattern search (SA needs O(m log n) binary search)
  - Easier to express certain algorithms (longest repeated substring, Ukkonen's online construction)
  - Supports more complex operations natively

**Rule of thumb**: Use SA unless you need online construction or the O(m) pattern search matters.

### Q2: Explain the time complexity of Dinic's algorithm and when it's optimal.

**Answer:**
Dinic's runs in O(V²E) in general because:
1. Each phase (BFS + blocking flow) increases the shortest augmenting path length by ≥1
2. So there are at most O(V) phases
3. Each blocking flow takes O(VE) using DFS with pointer advancement

For **unit-capacity networks**: O(E√V) because:
- The max flow ≤ V (all capacities 1)
- Each blocking flow sends ≥1 unit of flow
- After O(√E) phases, remaining flow ≤ √E; bipartite matching bound

For **bipartite matching**: Equivalent to unit-capacity network → O(E√V).

Practical performance is much better than worst-case due to early termination.

### Q3: What is the 2-SAT problem and how does SCC solve it?

**Answer:**
**2-SAT**: Given n boolean variables and m clauses each of form (x OR y) (literals can be negated), determine satisfying assignment.

**Reduction**: Each clause (a OR b) = (¬a → b) AND (¬b → a). Build implication graph with 2n nodes (xi and ¬xi for each variable).

**Solution via SCC**:
1. Find all SCCs using Tarjan's or Kosaraju's algorithm
2. For each variable xi: if xi and ¬xi are in the **same SCC** → UNSATISFIABLE
3. Otherwise: assign xi = True if SCC(xi) > SCC(¬xi) in topological order

```python
def two_sat(n, clauses):
    # Build implication graph: nodes 2i = xi, 2i+1 = NOT xi
    adj = [[] for _ in range(2*n)]
    for a, b in clauses:  # a, b are literals (positive = true, negative = negated)
        # clause (a OR b) = (NOT a → b) AND (NOT b → a)
        na = a ^ 1  # negate literal
        nb = b ^ 1
        adj[na].append(b)
        adj[nb].append(a)
    
    # Kosaraju's SCC
    order = []
    visited = [False] * (2*n)
    
    def dfs1(v):
        visited[v] = True
        for u in adj[v]:
            if not visited[u]: dfs1(u)
        order.append(v)
    
    radj = [[] for _ in range(2*n)]
    for v in range(2*n):
        for u in adj[v]: radj[u].append(v)
    
    for v in range(2*n):
        if not visited[v]: dfs1(v)
    
    comp = [-1] * (2*n)
    c = 0
    
    def dfs2(v, c):
        comp[v] = c
        for u in radj[v]:
            if comp[u] == -1: dfs2(u, c)
    
    for v in reversed(order):
        if comp[v] == -1:
            dfs2(v, c)
            c += 1
    
    # Check satisfiability and assign
    result = [False] * n
    for i in range(n):
        if comp[2*i] == comp[2*i+1]:
            return None  # unsatisfiable
        result[i] = comp[2*i] > comp[2*i+1]
    return result
```

### Q4: How does Mo's Algorithm achieve O((n+q)√n)?

**Answer:**
Mo's algorithm answers offline range queries by ordering them to minimize pointer movement.

**Key insight**: Sort queries by (block_of_left_endpoint, right_endpoint). For queries within the same block, right pointer moves monotonically → O(n) total right moves per block. Left pointer moves O(√n) within a block → O(q√n) total left moves.

```python
import math
from collections import defaultdict

def mo_algorithm(arr, queries):
    n = len(arr)
    block = int(math.sqrt(n))
    
    # Sort queries: (block_l, r) or (block_l, -r) for alternating
    indexed = [(l, r, i) for i, (l, r) in enumerate(queries)]
    indexed.sort(key=lambda x: (x[0]//block, x[1] if (x[0]//block)%2==0 else -x[1]))
    
    cur_l, cur_r = 0, -1
    freq = defaultdict(int)
    distinct = 0
    answers = [0] * len(queries)
    
    def add(idx):
        nonlocal distinct
        freq[arr[idx]] += 1
        if freq[arr[idx]] == 1: distinct += 1
    
    def remove(idx):
        nonlocal distinct
        freq[arr[idx]] -= 1
        if freq[arr[idx]] == 0: distinct -= 1
    
    for l, r, qi in indexed:
        while cur_r < r: cur_r += 1; add(cur_r)
        while cur_l > l: cur_l -= 1; add(cur_l)
        while cur_r > r: remove(cur_r); cur_r -= 1
        while cur_l < l: remove(cur_l); cur_l += 1
        answers[qi] = distinct
    
    return answers
```

**Total complexity**: O((n + q) × √n)
- Right pointer: O(n) moves per block × O(√n) blocks = O(n√n)
- Left pointer: O(√n) moves per query × O(q) queries = O(q√n)

---

## Quick Reference: Advanced Algorithm Patterns

```mermaid
graph LR
    A[Interval DP with monotone optimal split] -->|Check quad ineq| B[Knuth-Yao O(n²)]
    C[DP with linear cost function] -->|Slopes form hull| D[CHT O(n)]
    E[Multiple pattern matching] -->|Build automaton| F[Aho-Corasick]
    G[Suffix queries on string] -->|Build sorted suffixes| H[Suffix Array + LCP]
    I[Tree path queries] -->|Chain decompose| J[HLD + Seg Tree]
    K[Max flow in network] -->|Level graph| L[Dinic's O(V²E)]
    M[Boolean satisfiability 2-CNF] -->|Implication graph| N[2-SAT via SCC]
    O[Offline range queries] -->|Sort by sqrt block| P[Mo's O((n+q)√n)]
```
