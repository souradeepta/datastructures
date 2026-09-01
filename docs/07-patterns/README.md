# Interview Patterns — 39 Problems Organized by Pattern

Master 5 core patterns to solve 80% of interview questions.

---

## 🎯 The 5 Core Patterns

### 1️⃣ **Two-Pointer**
Traverse array from both ends or at different speeds.

**When to use:** Arrays, strings, linked lists  
**Problems:** 10 problems  
**Difficulty:** Easy-Medium  

→ [Learn More](two-pointer/)

### 2️⃣ **Sliding Window**
Maintain a dynamic window of elements.

**When to use:** Substrings, subarrays, fixed/variable window  
**Problems:** 9 problems  
**Difficulty:** Easy-Medium  

→ [Learn More](sliding-window/)

### 3️⃣ **Binary Search**
Divide and conquer with sorted data.

**When to use:** Sorted arrays, rotated arrays, boundary finding  
**Problems:** 8 problems  
**Difficulty:** Medium  

→ [Learn More](binary-search/)

### 4️⃣ **Monotonic Stack**
Stack with strictly increasing/decreasing elements.

**When to use:** Next/previous element, histogram problems  
**Problems:** 6 problems  
**Difficulty:** Medium-Hard  

→ [Learn More](monotonic-stack/)

### 5️⃣ **Prefix Sum / Range Query**
Pre-compute cumulative sums for fast range queries.

**When to use:** Subarray sum, range sum, 2D arrays  
**Problems:** 6 problems  
**Difficulty:** Medium  

→ [Learn More](prefix-sum/)

---

## 📊 All Patterns At a Glance

| Pattern | Count | Difficulty | Time | Space | Guide | Python |
|---------|-------|-----------|------|-------|-------|--------|
| Two-Pointer | 10 | Easy-Med | Varies | O(1) | [Guide](two-pointer/) | [Python](../../python/patterns/two_pointer.py) |
| Sliding Window | 9 | Easy-Med | O(n) | O(k) | [Guide](sliding-window/) | [Python](../../python/patterns/sliding_window.py) |
| Binary Search | 8 | Medium | O(log n) | O(1) | [Guide](binary-search/) | [Python](../../python/patterns/binary_search.py) |
| Monotonic Stack | 6 | Med-Hard | O(n) | O(n) | [Guide](monotonic-stack/) | [Python](../../python/patterns/monotonic_stack.py) |
| Prefix Sum | 6 | Medium | O(n) init | O(n) | [Guide](prefix-sum/) | [Python](../../python/patterns/prefix_sum.py) |

**Total: 39 problems**

---

## 🎯 Problem Difficulty Distribution

```
Easy (10-15%):
- Two-pointer basics
- Sliding window basics

Medium (70-75%):
- Most two-pointer advanced
- Most sliding window advanced
- Binary search
- Prefix sum

Hard (10-20%):
- Monotonic stack
- Complex pattern combinations
```

---

## 📁 Repository Structure

```
docs/07-patterns/
├── README.md (this file)
├── two-pointer/
│   ├── README.md (pattern guide)
│   ├── problems.md (10 problems)
│   └── problems.md (problem list)
python/patterns/ (maintained implementations)
tests/patterns/  (pytest coverage)
├── sliding-window/
│   ├── README.md
│   ├── problems.md
│   └── code/
├── binary-search/
├── monotonic-stack/
└── prefix-sum/
```

---

## 🚀 Learning Path

### Day 1-2: Two-Pointer
- Understand pattern
- Solve 3 easy problems
- Solve 2 medium problems

### Day 3-4: Sliding Window
- Understand fixed vs. variable window
- Solve 3 easy problems
- Solve 2 medium problems

### Day 5: Binary Search
- Understand search space
- Solve 3 medium problems
- Solve 1 hard problem

### Day 6: Monotonic Stack
- Understand stack property
- Solve 2 medium problems
- Solve 2 hard problems

### Day 7: Prefix Sum
- Understand cumulative sums
- Solve 2 medium problems
- Solve 1 hard problem

### Day 8-10: Mixed Practice
- Random problems from all patterns
- Identify pattern quickly
- Code under time pressure

---

## ✅ How to Use

1. **Pick pattern:** Start with two-pointer or sliding window
2. **Read guide:** `two-pointer/README.md` explains pattern
3. **See implementation:** `../../python/patterns/two_pointer.py` shows solutions
4. **Solve problems:** Complete `problems.md` problems
5. **Run tests:** `pytest tests/patterns/test_two_pointer.py`

---

## 💡 Interview Tips

**During interview:**
1. **Identify pattern** (2-3 min)
2. **Discuss approach** with interviewer (2-3 min)
3. **Code solution** (10-15 min)
4. **Test & optimize** (5-10 min)

**Pattern identification:**
- Two-pointer: "manipulate array in place" or "pair/triplet"
- Sliding window: "subarray", "max/min in window", "at most/at least"
- Binary search: "sorted array", "find target", "condition-based search"
- Monotonic stack: "next greater", "previous smaller", "histogram"
- Prefix sum: "range sum", "subarray sum", "2D prefix"

---

## 📊 Stats

- **Total problems:** 39
- **Easy:** 5
- **Medium:** 28
- **Hard:** 6
- **Tested core:** Yes (218 tests passing across the repository)
- **Language:** Python

---

**Ready for interviews!** Master these 5 patterns and you'll handle 80%+ of array/string problems.

---

**Last updated:** 2026-05-22
