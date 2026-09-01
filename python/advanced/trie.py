"""
Prefix Trie (Digital Search Tree)
===================================
A tree where each path from root to a terminal node spells out a word stored
in the trie. Efficient for prefix-based search, autocomplete, and spell-check.

Each node stores a mapping of characters to child nodes plus an end-of-word
flag.

Complexities  (m = length of the query/insert string, n = number of words):
    - insert:        O(m)
    - search:        O(m)
    - starts_with:   O(m)
    - delete:        O(m)
    - get_all_words: O(n * m_avg)
    - Space:         O(n * m_avg * alphabet_size)  worst case;
                     shared prefixes reduce this considerably in practice.
"""

from __future__ import annotations
from typing import Dict, List, Optional


class TrieNode:
    """
    A single node in the Trie.

    Attributes:
        children: map from character to child TrieNode.
        is_end:   True if this node terminates a stored word.
    """

    def __init__(self) -> None:
        self.children: Dict[str, TrieNode] = {}
        self.is_end: bool = False

    def __repr__(self) -> str:
        keys = list(self.children.keys())
        return f"TrieNode(end={self.is_end}, children={keys})"


class Trie:
    """
    Prefix Trie supporting insert, exact-search, prefix-check, delete,
    full word enumeration, and ASCII tree visualization.
    """

    def __init__(self) -> None:
        self._root = TrieNode()

    # ------------------------------------------------------------------
    # Insert
    # ------------------------------------------------------------------

    def insert(self, word: str) -> None:
        """
        Insert *word* into the trie.

        Time:  O(m) where m = len(word)
        Space: O(m) new nodes worst-case (all characters novel)
        """
        node = self._root
        for ch in word:
            if ch not in node.children:
                node.children[ch] = TrieNode()
            node = node.children[ch]
        node.is_end = True

    # ------------------------------------------------------------------
    # Search
    # ------------------------------------------------------------------

    def search(self, word: str) -> bool:
        """
        Return True if *word* was inserted (exact match required).

        Time:  O(m)
        Space: O(1)
        """
        node = self._find_node(word)
        return node is not None and node.is_end

    def starts_with(self, prefix: str) -> bool:
        """
        Return True if any inserted word begins with *prefix*.

        Time:  O(m) where m = len(prefix)
        Space: O(1)
        """
        return self._find_node(prefix) is not None

    def _find_node(self, prefix: str) -> Optional[TrieNode]:
        """Walk the trie along *prefix*; return the last node or None."""
        node = self._root
        for ch in prefix:
            if ch not in node.children:
                return None
            node = node.children[ch]
        return node

    # ------------------------------------------------------------------
    # Delete
    # ------------------------------------------------------------------

    def delete(self, word: str) -> bool:
        """
        Remove *word* from the trie. Returns True on success, False if
        the word was not present.

        Strategy (recursive):
          - Walk down to the last character.
          - On the way back up, remove child nodes that are no longer
            needed (no other words share that branch).

        Time:  O(m)
        Space: O(m) call stack
        """
        # The recursive helper returns whether a node can be pruned, not
        # whether the requested word existed.  Check presence first so a
        # successful deletion is reported even when shared nodes remain.
        if not self.search(word):
            return False
        self._delete(self._root, word, 0)
        return True

    def _delete(self, node: Optional[TrieNode], word: str, depth: int) -> bool:
        """Return True if the current node should be deleted by its parent."""
        if node is None:
            return False
        if depth == len(word):
            if not node.is_end:
                return False  # word not in trie
            node.is_end = False
            # Delete this node only if it has no children.
            return len(node.children) == 0
        ch = word[depth]
        if ch not in node.children:
            return False
        should_delete_child = self._delete(node.children[ch], word, depth + 1)
        if should_delete_child:
            del node.children[ch]
            # Delete this node if it's not end of another word and has no other children.
            return not node.is_end and len(node.children) == 0
        return False

    # ------------------------------------------------------------------
    # Enumerate all words
    # ------------------------------------------------------------------

    def get_all_words(self) -> List[str]:
        """
        Return a sorted list of every word stored in the trie.

        Time:  O(n * m_avg)
        Space: O(n * m_avg) for the output list
        """
        words: List[str] = []
        self._dfs(self._root, [], words)
        return sorted(words)

    def _dfs(
        self, node: TrieNode, path: List[str], words: List[str]
    ) -> None:
        if node.is_end:
            words.append("".join(path))
        for ch, child in node.children.items():
            path.append(ch)
            self._dfs(child, path, words)
            path.pop()

    # ------------------------------------------------------------------
    # ASCII visualization
    # ------------------------------------------------------------------

    def __str__(self) -> str:
        """
        Print the trie as an indented tree.

        Example for ["cat", "car", "card", "care", "dog"]:
            (root)
            ├── c
            │   └── a
            │       ├── t*
            │       └── r*
            │           ├── d*
            │           └── e*
            └── d
                └── o
                    └── g*
        (asterisk marks end-of-word nodes)
        """
        lines: List[str] = ["(root)"]
        children = sorted(self._root.children.items())
        for i, (ch, child) in enumerate(children):
            is_last = i == len(children) - 1
            self._build_str(ch, child, "", is_last, lines)
        return "\n".join(lines)

    def _build_str(
        self,
        ch: str,
        node: TrieNode,
        prefix: str,
        is_last: bool,
        lines: List[str],
    ) -> None:
        connector = "└── " if is_last else "├── "
        marker = "*" if node.is_end else ""
        lines.append(prefix + connector + ch + marker)
        extension = "    " if is_last else "│   "
        children = sorted(node.children.items())
        for i, (c, child) in enumerate(children):
            self._build_str(c, child, prefix + extension, i == len(children) - 1, lines)


# ----------------------------------------------------------------------
# Demo
# ----------------------------------------------------------------------

if __name__ == "__main__":
    trie = Trie()
    words = ["apple", "app", "application", "apply", "apt", "bat", "bad", "bag"]
    print("=== Trie ===")
    print("Inserting:", words)
    for w in words:
        trie.insert(w)

    print()
    print(trie)
    print()
    print("search('app')        :", trie.search("app"))
    print("search('ap')         :", trie.search("ap"))
    print("starts_with('ap')    :", trie.starts_with("ap"))
    print("starts_with('xyz')   :", trie.starts_with("xyz"))
    print()
    print("All words:", trie.get_all_words())
    print()
    trie.delete("app")
    print("After deleting 'app':")
    print("search('app')        :", trie.search("app"))
    print("search('apple')      :", trie.search("apple"))
    print("All words:", trie.get_all_words())
