# RAG Retrieval, Provenance, and Context Budgets

**Audience:** L4–L5 AI-systems candidates. **Practice time:** 25 minutes.

## Objective

Connect lexical retrieval to chunk provenance and a bounded prompt context while
being precise about what citations do—and do not—prove.

```text
documents -> chunks -> lexical index -> ranked chunks -> budgeted context
                                      \-> citation metadata
```

[`RAGPipeline`](../../python/ml_systems/rag_pipeline.py) tokenizes text
deterministically, scores chunks by query-term overlap, preserves insertion
order for ties, removes stale postings on re-index, and returns a citation for
each retrieved chunk. `build_context` admits whole chunks until its approximate
whitespace-token budget is exhausted.

A citation identifies source material that was retrieved; it does **not** prove
that an answer is factually correct or that a model used the source faithfully.
Production evaluation should measure retrieval recall/precision, answer
faithfulness, citation correctness, latency, cost, prompt-injection resistance,
access-control filtering, and freshness. This lab has no embeddings, generation,
reranking, persistence, ACLs, or untrusted-content isolation.

**Exercise:** add a gold-question fixture and report retrieval recall separately
from answer quality.
