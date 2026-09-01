"""A normalized, in-memory inverted index for system-design practice."""

from __future__ import annotations

import re
from collections import OrderedDict, defaultdict
from typing import DefaultDict, Hashable, List


TOKEN_RE = re.compile(r"\w+", re.UNICODE)


def _tokens(text: str) -> List[str]:
    return TOKEN_RE.findall(text.casefold())


class InvertedIndex:
    """Map normalized terms to document IDs while preserving document order."""

    def __init__(self) -> None:
        self.idx: DefaultDict[str, List[Hashable]] = defaultdict(list)
        self._doc_terms: dict[Hashable, set[str]] = {}
        self._doc_order: "OrderedDict[Hashable, None]" = OrderedDict()

    def index(self, did: Hashable, txt: str) -> None:
        """Insert or replace a document, removing all stale terms."""
        if not isinstance(txt, str):
            raise TypeError("document text must be a string")
        old_order = list(self._doc_order)
        old_position = old_order.index(did) if did in self._doc_order else None
        self.remove(did)
        terms = set(_tokens(txt))
        self._doc_terms[did] = terms
        if old_position is None:
            self._doc_order[did] = None
        else:
            old_order.insert(old_position, did)
            self._doc_order = OrderedDict((doc_id, None) for doc_id in old_order)
        for term in terms:
            self.idx[term].append(did)

    def remove(self, did: Hashable) -> bool:
        """Remove a document and its postings; return whether it existed."""
        if did not in self._doc_terms:
            return False
        for term in self._doc_terms.pop(did):
            postings = self.idx[term]
            self.idx[term] = [candidate for candidate in postings if candidate != did]
            if not self.idx[term]:
                del self.idx[term]
        del self._doc_order[did]
        return True

    def search(self, q: str) -> List[Hashable]:
        """Return insertion-ordered documents matching every query term."""
        if not isinstance(q, str):
            raise TypeError("query must be a string")
        terms = list(dict.fromkeys(_tokens(q)))
        if not terms or any(term not in self.idx for term in terms):
            return []
        matching = set(self.idx[terms[0]])
        for term in terms[1:]:
            matching.intersection_update(self.idx[term])
        return [did for did in self._doc_order if did in matching]


class SearchEngine:
    """Store document text and expose the normalized inverted-index API."""

    def __init__(self) -> None:
        self.idx = InvertedIndex()
        self.docs: "OrderedDict[Hashable, str]" = OrderedDict()

    def index_doc(self, did: Hashable, txt: str) -> None:
        self.idx.index(did, txt)
        self.docs[did] = txt

    def remove_doc(self, did: Hashable) -> bool:
        removed = self.idx.remove(did)
        if removed:
            del self.docs[did]
        return removed

    def search(self, q: str) -> List[Hashable]:
        return list(self.idx.search(q))


if __name__ == "__main__":
    engine = SearchEngine()
    engine.index_doc(1, "Python makes search practical.")
    print(engine.search("PYTHON"))
