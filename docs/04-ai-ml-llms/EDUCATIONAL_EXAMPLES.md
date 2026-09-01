# AI/ML Systems Educational Examples

These standard-library-only labs make three operational ML concepts runnable.
They are intentionally small in-memory teaching models, not model-training or
production-serving libraries.

- [Feature pipelines and parity](20-feature-pipelines-and-parity.md) —
  [implementation](../../python/ml_systems/feature_pipeline.py) ·
  [tests](../../tests/ml_systems/test_feature_pipeline.py)
- [RAG grounding and evaluation](21-rag-grounding-and-evaluation.md) —
  [implementation](../../python/ml_systems/rag_pipeline.py) ·
  [tests](../../tests/ml_systems/test_rag_pipeline.py)
- [Model rollouts and serving](22-model-rollouts-and-serving.md) —
  [implementation](../../python/ml_systems/model_rollout.py) ·
  [tests](../../tests/ml_systems/test_model_rollout.py)

Together they cover data leakage prevention, retrieval/provenance, context
budgets, canaries, quality gates, and operational guardrails. They do not
include a model, embeddings, GPUs, persistence, distributed coordination,
authentication, authorization, or production capacity claims.
