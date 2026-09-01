"""
Suffix Tree

Time Complexity:
- Construction: O(n) with Ukkonen's algorithm (simplified: O(n²) here)
- Pattern search: O(m) where m = pattern length
- Longest repeated substring: O(n² log n) with the simplified suffix ordering
- Substring counting: O(n)
- Space Complexity: O(n)

Use Cases:
- Pattern matching and substring search (faster than regex)
- Finding longest repeated substring
- Longest common substring of multiple strings
- String compression
- Palindrome detection

Key Insight:
- Compact trie of all suffixes
- Each edge has substring, not single character
- Linear space and time with Ukkonen's algorithm
- More complex to implement than suffix array
- Better for multiple queries on same string
"""

from typing import Optional, List, Dict, Tuple


class SuffixNode:
    """Node in suffix tree."""

    def __init__(self):
        self.children = {}
        self.suffix_link = None
        self.start = -1
        self.end = -1
        self.suffix_idx = -1


class SuffixTree:
    """Suffix tree for efficient string searching."""

    def __init__(self, text: str):
        """
        Build suffix tree from text.

        Args:
            text: Input string
        """
        self.text = text + "$"  # Add sentinel
        self.n = len(self.text)
        self.root = SuffixNode()
        self.root.start = -1
        self.root.end = 0

        # Build using simplified O(n²) approach
        self._build_tree()

    def _build_tree(self) -> None:
        """Build suffix tree by inserting all suffixes."""
        for i in range(self.n):
            self._insert_suffix(i)

    def _insert_suffix(self, suffix_idx: int) -> None:
        """Insert suffix starting at suffix_idx."""
        node = self.root
        i = suffix_idx

        while i < self.n:
            char = self.text[i]

            if char not in node.children:
                # Create new leaf
                leaf = SuffixNode()
                leaf.start = i
                leaf.end = self.n
                leaf.suffix_idx = suffix_idx
                node.children[char] = leaf
                break
            else:
                edge_node = node.children[char]
                edge_len = edge_node.end - edge_node.start

                # Check if suffix matches this edge
                match_len = 0
                while match_len < edge_len and i + match_len < self.n:
                    if self.text[edge_node.start + match_len] != self.text[i + match_len]:
                        break
                    match_len += 1

                if match_len == edge_len:
                    # Full edge match, continue with child
                    node = edge_node
                    i += edge_len
                else:
                    # Partial match, split edge
                    split_node = SuffixNode()
                    split_node.start = edge_node.start
                    split_node.end = edge_node.start + match_len
                    split_node.suffix_idx = -1

                    # Old edge becomes child
                    old_char = self.text[edge_node.start + match_len]
                    split_node.children[old_char] = edge_node
                    edge_node.start = split_node.end

                    # New leaf
                    leaf = SuffixNode()
                    leaf.start = i + match_len
                    leaf.end = self.n
                    leaf.suffix_idx = suffix_idx
                    split_node.children[self.text[i + match_len]] = leaf

                    # Replace edge
                    node.children[char] = split_node
                    break

    def search(self, pattern: str) -> List[int]:
        """
        Find all occurrences of pattern.

        Returns:
            List of starting positions
        """
        positions = []
        node = self.root
        i = 0

        # Traverse tree following pattern
        while i < len(pattern):
            char = pattern[i]

            if char not in node.children:
                return positions

            edge_node = node.children[char]
            edge_str = self.text[edge_node.start : edge_node.end]
            edge_len = len(edge_str)

            # Check if pattern matches this edge
            pattern_remaining = pattern[i:]
            match_len = 0

            while match_len < edge_len and match_len < len(pattern_remaining):
                if edge_str[match_len] != pattern_remaining[match_len]:
                    return positions
                match_len += 1

            i += match_len
            node = edge_node

        # Collect all leaf positions under this node
        self._collect_positions(node, positions)
        return sorted(positions)

    def _collect_positions(self, node: SuffixNode, positions: List[int]) -> None:
        """Collect suffix indices from all leaves under node."""
        if node.suffix_idx != -1:
            # Leaf node
            positions.append(node.suffix_idx)
        else:
            # Internal node
            for child in node.children.values():
                self._collect_positions(child, positions)

    def longest_repeated_substring(self) -> str:
        """Find the longest substring that appears at least twice.

        The builder above is intentionally a small educational suffix-tree
        implementation. To keep this query correct even when a repeated
        substring ends in the middle of an edge, compare adjacent suffixes in
        suffix order and retain their longest common prefix.
        """
        source = self.text[:-1]  # Never return the terminal sentinel.
        if not source:
            return ""

        suffixes = sorted(range(len(source)), key=lambda start: source[start:])
        best_start = -1
        best_length = 0

        for left, right in zip(suffixes, suffixes[1:]):
            length = 0
            while (
                left + length < len(source)
                and right + length < len(source)
                and source[left + length] == source[right + length]
            ):
                length += 1
            if length > best_length:
                best_start = left
                best_length = length

        if best_start == -1:
            return ""
        return source[best_start : best_start + best_length]

    def _count_leaves(self, node: SuffixNode) -> int:
        """Count leaves under node."""
        if node.suffix_idx != -1:
            return 1

        count = 0
        for child in node.children.values():
            count += self._count_leaves(child)

        return count


if __name__ == "__main__":
    # Example 1: Basic search
    print("=== Example 1: Pattern Search ===")
    text = "banana"
    tree = SuffixTree(text)

    patterns = ["ana", "na", "ban", "nana"]
    print(f"Text: '{text}'")
    for pattern in patterns:
        positions = tree.search(pattern)
        print(f"Pattern '{pattern}': positions {positions}")

    # Example 2: Longest repeated substring
    print("\n=== Example 2: Longest Repeated Substring ===")
    texts = ["banana", "abracadabra", "mississippi"]
    for t in texts:
        tree = SuffixTree(t)
        lrs = tree.longest_repeated_substring()
        print(f"Text '{t}': longest repeated = '{lrs}'")

    # Example 3: More complex text
    print("\n=== Example 3: Complex Text ===")
    text3 = "hello world hello"
    tree3 = SuffixTree(text3)

    patterns3 = ["hello", "world", "ll", "o w"]
    print(f"Text: '{text3}'")
    for pattern in patterns3:
        positions = tree3.search(pattern)
        print(f"Pattern '{pattern}': positions {positions}")
