"""A lexical, provenance-preserving RAG retrieval teaching model."""

from __future__ import annotations

import re
from copy import deepcopy
from dataclasses import dataclass
from typing import Any, Mapping


TOKEN_RE = re.compile(r"[A-Za-z0-9]+")


@dataclass(frozen=True)
class Chunk:
    chunk_id: str
    document_id: str
    text: str
    metadata: Mapping[str, Any]


@dataclass(frozen=True)
class RetrievedChunk:
    chunk: Chunk
    score: int
    citation: str


@dataclass(frozen=True)
class ContextBundle:
    text: str
    citations: tuple[str, ...]
    chunks: tuple[RetrievedChunk, ...]


class RAGPipeline:
    """Index whitespace-sized chunks and rank them by lexical overlap.

    The model preserves chunk provenance and limits context by approximate
    whitespace-token count. A citation identifies retrieved source material;
    it does not prove that generated text is factually grounded.
    """

    def __init__(self, max_context_tokens: int = 500) -> None:
        if not isinstance(max_context_tokens, int) or isinstance(max_context_tokens, bool) or max_context_tokens < 1:
            raise ValueError("max_context_tokens must be positive")
        self.max_context_tokens = max_context_tokens
        self._documents: dict[str, tuple[Chunk, ...]] = {}
        self._chunks: list[Chunk] = []

    @staticmethod
    def _tokens(text: str) -> list[str]:
        return [token.lower() for token in TOKEN_RE.findall(text)]

    def index_document(
        self, document_id: str, text: str, metadata: Mapping[str, Any] | None = None, chunk_size: int = 80
    ) -> tuple[Chunk, ...]:
        if not isinstance(document_id, str) or not document_id:
            raise ValueError("document_id must be a non-empty string")
        if not isinstance(text, str) or not text.strip():
            raise ValueError("text must be non-empty")
        if not isinstance(chunk_size, int) or isinstance(chunk_size, bool) or chunk_size < 1:
            raise ValueError("chunk_size must be positive")
        words = text.split()
        metadata_copy = deepcopy(dict(metadata or {}))
        chunks = tuple(
            Chunk(f"{document_id}:{index}", document_id, " ".join(words[start:start + chunk_size]), deepcopy(metadata_copy))
            for index, start in enumerate(range(0, len(words), chunk_size))
        )
        self.remove_document(document_id)
        self._documents[document_id] = chunks
        self._chunks.extend(chunks)
        return tuple(deepcopy(chunks))

    def remove_document(self, document_id: str) -> bool:
        if document_id not in self._documents:
            return False
        del self._documents[document_id]
        self._chunks = [chunk for chunk in self._chunks if chunk.document_id != document_id]
        return True

    def retrieve(self, query: str, top_k: int = 5) -> tuple[RetrievedChunk, ...]:
        if not isinstance(query, str) or not query.strip():
            raise ValueError("query must be non-empty")
        if not isinstance(top_k, int) or isinstance(top_k, bool) or top_k < 1:
            raise ValueError("top_k must be positive")
        terms = set(self._tokens(query))
        scored = []
        for position, chunk in enumerate(self._chunks):
            score = sum(1 for term in terms if term in set(self._tokens(chunk.text)))
            if score:
                scored.append((-(score), position, RetrievedChunk(deepcopy(chunk), score, f"[{chunk.document_id}:{chunk.chunk_id.split(':')[-1]}]")))
        scored.sort(key=lambda item: (item[0], item[1]))
        return tuple(item[2] for item in scored[:top_k])

    def build_context(self, results: tuple[RetrievedChunk, ...] | list[RetrievedChunk], max_tokens: int | None = None) -> ContextBundle:
        budget = self.max_context_tokens if max_tokens is None else max_tokens
        if not isinstance(budget, int) or isinstance(budget, bool) or budget < 1:
            raise ValueError("max_tokens must be positive")
        chosen = []
        used = 0
        for result in results:
            tokens = len(self._tokens(result.chunk.text))
            if used + tokens > budget:
                continue
            chosen.append(deepcopy(result))
            used += tokens
        return ContextBundle(
            text="\n\n".join(result.chunk.text for result in chosen),
            citations=tuple(result.citation for result in chosen),
            chunks=tuple(chosen),
        )
