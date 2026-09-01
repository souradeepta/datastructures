# Feature Pipelines and Point-in-Time Parity

**Audience:** L4–L5 ML-systems candidates. **Practice time:** 25 minutes.

## Objective

Show how training examples can leak future information, and design one feature
contract that works for both historical training and online lookup.

```text
events -> validation -> timestamped feature history -> as-of lookup
                                      ^ cutoff prevents future leakage
```

[`FeaturePipeline`](../../python/ml_systems/feature_pipeline.py)
validates a declared feature schema, accepts out-of-order events, and returns
the latest value whose timestamp is at or before an `as_of_ms` cutoff. Missing
features are omitted rather than filled silently, and returned values are copy
isolated.

The model is in-memory and dependency-free. Production parity requires a
shared transformation definition, offline/online stores, freshness monitoring,
backfills, schema/version management, point-in-time joins across sources,
privacy controls, and a policy for missing values.

**Exercise:** add feature freshness metadata and make the caller distinguish a
missing feature from a stale feature.
