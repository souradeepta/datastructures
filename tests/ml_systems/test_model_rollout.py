import pytest

from python.ml_systems.model_rollout import ModelRollout


def test_assignment_is_stable_and_percentage_is_validated():
    rollout = ModelRollout("v1", "v2", candidate_percentage=50)
    assert rollout.version_for("user-1") == rollout.version_for("user-1")
    assert {rollout.version_for(f"user-{i}") for i in range(100)} == {"v1", "v2"}
    with pytest.raises(ValueError):
        rollout.set_candidate_percentage(101)


def test_failed_quality_and_online_guardrails_block_promotion():
    rollout = ModelRollout("v1", "v2", min_quality=0.8, max_latency_ms=100, max_error_rate=0.1)
    rollout.record_observation(150)
    with pytest.raises(RuntimeError, match="quality"):
        rollout.promote(0.7)
    with pytest.raises(RuntimeError, match="guardrail"):
        rollout.promote(0.9)


def test_promotion_and_rollback():
    rollout = ModelRollout("v1", "v2", candidate_percentage=20, min_quality=0.8)
    rollout.record_observation(50)
    rollout.promote(0.9)
    assert rollout.baseline_version == "v2"
    assert rollout.candidate_percentage == 0
    rollout.rollback()
    assert rollout.baseline_version == "v1"
    assert rollout.candidate_version == "v2"
    assert rollout.candidate_percentage == 0


def test_observation_errors_and_invalid_configuration():
    with pytest.raises(ValueError):
        ModelRollout("v1", "v2", max_error_rate=2)
    rollout = ModelRollout("v1", "v2")
    rollout.record_observation(10, error=True)
    assert rollout.error_rate == 1.0
    with pytest.raises(ValueError):
        rollout.version_for("")
    with pytest.raises(RuntimeError, match="dependency failed"):
        rollout.serve("user", lambda _version: (_ for _ in ()).throw(RuntimeError("dependency failed")))
