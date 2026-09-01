# Model Rollouts and Serving Guardrails

**Audience:** L4–L5 ML-systems candidates. **Practice time:** 25 minutes.

## Objective

Design a canary rollout with stable user assignment, offline quality gates,
online latency/error guardrails, and rollback.

```text
user id -> stable hash bucket -> baseline or candidate -> observations
                                              quality + guardrails -> promote
                                                                    \-> rollback
```

[`ModelRollout`](../../python/ml_systems/model_rollout.py) uses a salted
SHA-256 bucket, explicit baseline/candidate versions, a candidate percentage,
and recorded observations. Promotion requires the configured offline quality,
average latency, and error-rate gates. `serve` invokes a selected model
callback and deliberately propagates its errors; rollback removes candidate
traffic.

This is not a serving stack. Production rollouts need model/package integrity,
feature compatibility, shadow traffic, cohort and fairness analysis, regional
capacity, autoscaling, timeout budgets, privacy controls, audit logs, alerting,
and a rollback that restores the exact prior artifact and configuration.

**Exercise:** add a minimum sample-size gate and compare global bucketing with
region-aware assignment.
