# Coding Interview Framework: 45-Minute Problem Solving

**Level:** L3-L5
**Status:** draft
**Audience:** Candidate practicing 45-minute coding interviews for L3–L5 roles.
**Prerequisites:** Python control flow, common data structures, asymptotic notation, and a test runner.
**Sequence:** Batch 4A, 3/4
**Terra gate:** open
**Time to read:** ~20 min

A proven 5-step framework for solving algorithmic problems in 45-minute technical interviews.

## Learning objectives

- Turn an ambiguous prompt into explicit input, output, constraint, and edge-case requirements.
- State a brute-force baseline before selecting a pattern and proving its invariant.
- Implement, test, and debug a solution while narrating complexity and trade-offs.
- Use a timed retrospective to identify whether the bottleneck was understanding, algorithm choice, coding, or verification.

## Expected outputs

For each practice problem, record the clarification contract, brute-force idea,
optimized invariant, complexity, three edge-case tests, and one retrospective
note. Reviewers should be able to distinguish a correct solution from a lucky
sample pass. Link implementations to the maintained Python tree when one exists.

## Review checkpoints

- **5 minutes:** input/output and constraints are confirmed.
- **10 minutes:** baseline and optimized approach are compared with complexity.
- **35 minutes:** code handles normal and boundary cases with tests.
- **45 minutes:** correctness invariant, complexity, and one alternative are explained.

---

## Phase 1: Clarify & Verify (5 minutes)

**Goal:** Understand the problem completely before coding. This phase prevents you from solving the wrong problem.

### Questions to Ask (In Order)

**Input/Output (Most Important):**
- "What's the input format? (array, string, tree, graph, matrix, linked list)"
- "What are the constraints on input size? (1 ≤ n ≤ 10^5?)"
- "What should I return? (single value, list, count, boolean, path)"
- "Can the input be empty/null? What should I return in that case?"
- "Are there any restrictions on the values? (positive only, integers, floats)"

**Constraints & Properties:**
- "Are there negative numbers?"
- "Can there be duplicates?"
- "What's the maximum value of n? (10^3, 10^5, 10^6)"
- "Is the input sorted or unsorted?"
- "Are there repeated elements?"
- "Should I modify the input or keep it unchanged?"

**Performance Requirements:**
- "Is there a specific time or space target? (under 1 second, under 100MB)"
- "Would O(n log n) be acceptable or do I need O(n)?"
- "Is O(n²) too slow? (depends on n)"
- "Can I use extra space or must it be O(1)?"

**Domain-Specific:**
- For arrays: "Contiguous subarrays or subsequences? Order matter?"
- For strings: "Case sensitive? Unicode characters?"
- For trees/graphs: "Directed or undirected? Cyclic?"
- For linked lists: "Singly or doubly linked?"

### Real Example Walkthrough

**Problem:** "Find the two sum in a sorted array that adds up to target"

**Good Clarification Dialogue:**
```
You: "So I need to find two numbers that add to the target?"
Interviewer: "Yes"
You: "And the array is sorted?"
Interviewer: "Yes"
You: "Should I return the indices or the values?"
Interviewer: "Indices, 0-indexed"
You: "Are there guaranteed to be two numbers that sum to target?"
Interviewer: "Yes, exactly one pair"
You: "Can there be duplicates in the array?"
Interviewer: "Yes"
You: "And the array is sorted in ascending order?"
Interviewer: "Yes"
```

### Template to Fill Out

```
Problem: [Name]

Input Format: [array of size n, string, etc]
Output Format: [indices, count, modified array, etc]

Constraints:
- n: _____
- Value range: _____
- Duplicates: Yes/No
- Sorted: Yes/No/Unknown
- Can modify input: Yes/No
- Target time: O(?)
- Target space: O(?)

Examples:
Input: [values], target = X
Output: [expected result]

Input: [edge case], target = X
Output: [expected result]

Edge Cases:
- Empty input: return ___
- Single element: return ___
- All duplicates: return ___
```

### Critical Mistakes to Avoid in Phase 1

| Mistake | Impact | Fix |
|---------|--------|-----|
| Assuming sorted when not stated | Wrong algorithm | Always ask |
| Not asking about duplicates | Algorithm breaks | Always ask |
| Forgetting to clarify return type | Wrong solution | Explicitly confirm |
| Assuming single answer exists | Crashes on multiple answers | Ask about edge cases |
| Not confirming constraints | O(n²) fails on n=10^5 | Ask max n |

---

## Phase 2: Think Aloud (2-3 minutes)

**Goal:** Show your thinking process. Avoid silent coding.

### Approach to Discuss

**Brute Force First:**
- "Naive approach: [O(n²) solution]"
- Explain the idea, even if it's not optimal

**Identify Pattern:**
- "I notice this looks like a [DP/BFS/greedy] problem"
- "This is similar to [known pattern] because..."

**Optimize:**
- "Can I use [data structure] to improve to O(n log n)?"
- "What trade-off am I making (time vs. space)?"

### Real Interview Dialogue Example

**Problem:** "Find all unique pairs in an array that sum to a target"

**Interviewer:** "You have 15 minutes for this problem."

**You:** "Let me break this down. So I need to find all pairs [a, b] where a + b = target?"

**Interviewer:** "Yes, and all pairs should be unique."

**You:** "Got it. Let me think about the brute force first. I could check every pair - nested loops would be O(n²) time, O(1) space if I count pairs. That works but it's not great.

But I notice with two pointers on a sorted array, I could do O(n log n + sort) with O(1) extra space. Or I could use a hash set: iterate through, and for each element x, check if target - x is in the set. That's O(n) time but O(n) space.

Given the constraints, I'll go with the hash set approach since time is more important than space here. Let me code that up."

**Interviewer:** "Good thinking. Let's see the code."

### Red Flags to Avoid

- ❌ Silent coding with no explanation
- ❌ Jumping to code without discussing approach
- ❌ Implementing complex solution without verifying idea first
- ❌ Over-optimizing prematurely
- ❌ Proposing solution without understanding trade-offs

**Green Flags to Show**

- ✅ "Let me verify my understanding first"
- ✅ "My brute force is O(n²), let me optimize to..."
- ✅ "I'll use [structure] because it gives me O(?) complexity"
- ✅ "Let me trace through an example to verify"
- ✅ "There are two approaches: X is faster but needs more space, Y is simpler..."

---

## Phase 3: Code Cleanly (25-30 minutes)

**Goal:** Write readable, bug-free code.

### Structure to Follow

```
1. Function signature with clear parameter names
2. Input validation (if time permits)
3. Initialize data structures
4. Main logic (clearly structured)
5. Return result
```

### Best Practices

**Naming:**
- Use descriptive variable names (not `i`, `x`, `temp`)
- Avoid single-letter vars except loop counters
- Index variables: `left`/`right` (not `l`/`r`), `start`/`end`

**Structure:**
- Break into helper functions if >20 lines
- Use comments for non-obvious steps only
- Keep indentation consistent
- Group related logic (e.g., validation before processing)

**Avoid Common Mistakes:**
- Off-by-one errors: use `i < n` not `i <= n` (verify bounds)
- Null pointer checks: handle `None` / `null` cases
- Integer overflow: use `//` for integer division, watch modulo
- Mutable default arguments: `def func(arr=[])` is bad
- Not returning the right type (int vs list vs boolean)

### Common Mistakes During Coding

| Mistake | Example | Fix |
|---------|---------|-----|
| Forgetting to skip duplicates | Finding pairs of (1,2) and (2,1) | Use set to track seen pairs |
| Off-by-one in loop | `for i in range(len(arr)-1)` missing last element | Think: what happens at boundary? |
| Modifying input implicitly | Sorting in-place when told not to | Check constraints first, copy if needed |
| Wrong variable initialization | `result = None` then `.append()` | Initialize to correct type: `[]` or `set()` |
| Not handling edge case | Empty array → IndexError | Validate input at start |

### Python Template

```python
def solve(arr, target):
    # Validate input
    if not arr:
        return []
    
    # Initialize
    result = []
    seen = set()
    
    # Main logic
    for num in arr:
        if num not in seen:
            # Process
            result.append(num)
            seen.add(num)
    
    return result
```

### Java Template

```java
public class Solution {
    public int[] solve(int[] arr, int target) {
        // Validate
        if (arr == null || arr.length == 0) {
            return new int[]{};
        }
        
        // Initialize
        List<Integer> result = new ArrayList<>();
        Set<Integer> seen = new HashSet<>();
        
        // Main logic
        for (int num : arr) {
            if (!seen.contains(num)) {
                result.add(num);
                seen.add(num);
            }
        }
        
        // Convert and return
        return result.stream().mapToInt(i -> i).toArray();
    }
}
```

---

## Phase 4: Test & Verify (5-8 minutes)

**Goal:** Ensure correctness before submitting.

### Test Cases to Run

**Happy Path:**
- Example given in problem statement
- Trace through your code step-by-step
- Include problem's exact inputs/outputs

**Edge Cases:**
- Empty input: `[]`, `""`, `None`
- Single element: `[5]`
- Two elements: `[1, 2]`
- Duplicates: `[1, 1, 1]`
- Negatives: `[-5, 0, 5]`
- Boundary values: `[0, MAX_INT, MIN_INT]`
- All same: `[5, 5, 5, 5]`
- Already sorted: `[1, 2, 3]`
- Reverse sorted: `[3, 2, 1]`

### Real Testing Example

**Problem:** Find all pairs summing to target, target = 5

```
Test 1 (Happy Path):
Input: [2, 3, 1, 4], target = 5
Expected: [(2,3), (1,4)] or similar
Trace:
  num=2: target-2=3, not seen. seen={2}
  num=3: target-3=2, FOUND! (2,3). seen={2,3}
  num=1: target-1=4, not seen. seen={2,3,1}
  num=4: target-4=1, FOUND! (1,4). seen={2,3,1,4}
Result: [(2,3), (1,4)] ✓

Test 2 (Edge Case - Duplicates):
Input: [2, 2, 3, 3], target = 5
Should return: [(2,3)] (unique pairs only)
Trace: First (2,3) added to set, second (2,3) skipped (already exists)
Result: [(2,3)] ✓

Test 3 (Edge Case - No pairs):
Input: [1, 2], target = 10
Expected: []
Result: [] ✓

Test 4 (Edge Case - Empty):
Input: [], target = 5
Expected: []
Result: [] ✓
```

### Verification Checklist

- ✓ Code compiles/runs without syntax errors
- ✓ Happy path example produces correct output
- ✓ Edge cases handled (empty, single, negatives, max, duplicates)
- ✓ No off-by-one errors in loops
- ✓ Variable initializations are correct
- ✓ Return statement is correct
- ✓ Traced through at least one example by hand
- ✓ No unhandled null/None cases

---

## Phase 5: Complexity & Discussion (5-10 minutes)

**Goal:** Articulate time/space complexity and discuss improvements.

### Complexity Calculation

**Time Complexity:**
- Identify the dominant loop/operation
- Count iterations: "I loop through n elements once: O(n)"
- Count nested loops: "For each of n, I do log n binary search: O(n log n)"
- Add asymptotics: "O(n) iteration + O(1) per element = O(n)"
- Watch out for: hidden loops, recursive calls, data structure operations

**Space Complexity:**
- Hash set storing n elements: O(n)
- Recursion depth d on call stack: O(d)
- Output array of size m: O(m)
- Don't count input in analysis (already provided)

**Example Explanation:**

```
Problem: Find pairs summing to target

Time: O(n) - one pass through array, hash set operations are O(1)
Space: O(n) - hash set stores up to n elements, pairs output is O(k) where k = num pairs

Can we do better?
- Time: Already optimal (must look at each element at least once)
- Space: With sorted input + two pointers: O(1) but requires sorting (O(n log n))
- Trade-off: My approach O(n) time + O(n) space is best for unsorted input
```

### Common Complexity Mistakes

| Mistake | Example | Correct |
|---------|---------|---------|
| Forgetting sorting cost | "Two pointers O(n) space" | Don't forget O(n log n) sort if needed |
| Confusing hash operations | "Hash set is O(1) per operation" | True on average, O(n) worst case with collisions |
| Not counting output | "Remove duplicates is O(n) space" | Also count the output array |
| Recursive calls | "DFS is O(n)" | Also count recursion stack O(h) height |
| Nested data structures | "Store all pairs in set" | Sets have O(1) lookup but O(n) space for all pairs |

### Follow-up Optimization Questions

**If you finished with time left (best case):**
```
You: "I've verified correctness. Would you like me to optimize further?"

Interviewer: "Sure, can you improve space complexity?"

You: "With a sorted array, I could use two pointers:
- Sort: O(n log n) time
- Two pointers: O(n) time
- Result: O(n log n) total, O(1) space (excluding output)

Should I implement this version?"
```

**If you struggled with bugs (recovery):**
```
You: "I found a bug in the duplicate handling. Let me fix it."

[Add a check to skip duplicate pairs]

You: "There - now the set tracks seen pairs instead of seen numbers.
Let me re-trace the duplicate example... Yes, this now returns one (2,3) instead of duplicates."
```

### When NOT to Optimize

- ✗ Don't optimize prematurely (interviewer didn't ask)
- ✗ Don't introduce complexity if time is running out
- ✓ Wait for interviewer signal: "Can you improve?" or "Any follow-ups?"
- ✓ Mention optimizations in discussion ("could use two pointers if sorted")

---

## Communication During Interview

### What to Say

| Situation | What to Say |
|-----------|-----------|
| **Stuck on approach** | "Let me think about this... [pause] The brute force would be... [explain]. Can I optimize?" |
| **Found a pattern** | "I notice this is similar to [problem pattern]." |
| **Trade-off decision** | "I'm choosing O(n) time and O(n) space because the time constraint is more important here." |
| **Found a bug** | "Wait, let me trace through this again... I see the issue is [explain]." |
| **Don't know solution** | "I'm not sure of the optimal approach. Let me code the brute force first: [explain]." |
| **Time running out** | "I see we're running short. Let me [finish core logic / explain remaining approach]." |

### Red Flags to Avoid

| Mistake | Why It Hurts |
|---------|-------------|
| Silent for 10+ minutes | Interviewer can't follow your thinking |
| Coding without planning | Leads to bugs, wastes time rewriting |
| Not asking clarifying questions | Miss constraints, solve wrong problem |
| Ignoring edge cases | Solution fails on simple inputs |
| Off-by-one errors | Code doesn't compile or fails test |
| Blaming the problem | "This problem is ambiguous" (even if true) |

---

## Problem Categories & Patterns

### Arrays & Strings

| Pattern | Time | Approach |
|---------|------|----------|
| Two pointers | O(n) | Converge from ends |
| Sliding window | O(n) | Fixed/dynamic window |
| Prefix sum | O(n) | Precompute cumulative |
| Hashing | O(n) | Store in set/dict |
| Sorting | O(n log n) | Sort then solve |

### Trees & Graphs

| Pattern | Time | Approach |
|---------|------|----------|
| BFS | O(n+e) | Level-order queue |
| DFS | O(n+e) | Recursive traversal |
| Binary search tree | O(log n) avg | Leverage BST property |
| Union-Find | O(α(n)) | Track components |
| Topological sort | O(n+e) | DFS/Kahn's |

### Dynamic Programming

| Pattern | Time | Approach |
|---------|------|----------|
| 1D DP | O(n) | Recurrence on prev state |
| 2D DP | O(n²) | Table filling |
| Backtracking | O(k^n) | Explore all choices |
| Memoization | O(states) | Cache results |

---

## Coding Interview Checklist

- ✓ Ask clarifying questions (constraints, edge cases)
- ✓ Think aloud about approach before coding
- ✓ Start with brute force, then optimize
- ✓ Use clear variable names and structure
- ✓ Trace through example while coding
- ✓ Handle edge cases (empty, single, negatives, max)
- ✓ Test code on provided examples
- ✓ Discuss time and space complexity
- ✓ Explain trade-offs in your solution
- ✓ Ask if interviewer wants further optimization

---

## Interview Checklist by Time

| Time | Action |
|------|--------|
| 0-5 min | Clarify problem, ask questions, verify understanding |
| 5-10 min | Discuss approach, draw examples, get agreement |
| 10-35 min | Code cleanly, trace through examples, fix bugs |
| 35-40 min | Test on edge cases, verify correctness |
| 40-45 min | Discuss complexity, mention optimizations, wrap up |
