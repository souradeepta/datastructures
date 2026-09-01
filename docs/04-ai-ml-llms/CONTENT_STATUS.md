# AI/ML systems content status

This directory contains 22 long-form AI/ML/LLM study guides plus three runnable
labs. The count excludes `README.md`, this page, and `EDUCATIONAL_EXAMPLES.md`.
The long-form guides are not uniformly reviewed or backed by executable
implementations. The three labs are part of the repository’s six runnable
distributed/ML systems labs overall.

## Status definitions

- **Tested:** A focused pytest test exercises the documented educational API.
  This validates the example contract; it does not establish production
  readiness.
- **Reviewed:** A maintainer has manually checked the guide’s objective,
  assumptions, calculations, trade-offs, failure modes, and links.
- **Draft:** Useful study material that has not passed the reviewed standard;
  examples or calculations may be incomplete.

No broad reviewed status is claimed for this directory. The labs are **tested**;
the long-form guides should be treated as **draft** unless a future guide-level
review records otherwise.

## Implementation and test links

| Lab | Implementation | Focused tests | Outcome |
|---|---|---|---|
| Feature pipelines and parity | [feature_pipeline.py](../../python/ml_systems/feature_pipeline.py) | [test_feature_pipeline.py](../../tests/ml_systems/test_feature_pipeline.py) | Detect future-data leakage and preserve point-in-time feature parity. |
| RAG grounding and evaluation | [rag_pipeline.py](../../python/ml_systems/rag_pipeline.py) | [test_rag_pipeline.py](../../tests/ml_systems/test_rag_pipeline.py) | Keep chunk provenance, retrieval scores, and context budgets explicit. |
| Model rollouts and serving | [model_rollout.py](../../python/ml_systems/model_rollout.py) | [test_model_rollout.py](../../tests/ml_systems/test_model_rollout.py) | Exercise stable canary assignment and promotion safety gates. |

The [educational examples guide](EDUCATIONAL_EXAMPLES.md) explains the contracts
and connects each lab to the related long-form material.

## Verification

Run the focused ML/AI lab suite with:

```bash
pytest tests/ml_systems -q
```

Run the full maintained suite and import/link gate with:

```bash
pytest -q
python3 scripts/validate_repo.py --imports
```

## Known limitations

These are standard-library-only, in-memory teaching models. They do not provide
trained models, real embeddings, GPUs, persistence, distributed coordination,
concurrency controls, authentication, authorization, model governance, online
feature stores, or production capacity/reliability guarantees. RAG retrieval is
lexical rather than embedding-based, and rollout behavior is a deterministic
simulation rather than a deployment controller.

## Next review priorities

1. Manually review the 22 long-form guides using the reviewed checklist and mark
   guide-level status explicitly.
2. Reconcile older LLMOps, serving, and RAG claims with the runnable lab
   contracts and their stated limitations.
3. Add failure-mode and evaluation exercises for data freshness, feature skew,
   retrieval quality, model rollback, and cost/latency trade-offs.
