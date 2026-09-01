import pytest

from python.ml_systems.feature_pipeline import FeaturePipeline


def test_point_in_time_snapshot_handles_out_of_order_events():
    pipeline = FeaturePipeline({"age": int, "score": float})
    pipeline.ingest("u1", "age", 20, 31)
    pipeline.ingest("u1", "age", 10, 30)
    pipeline.ingest("u1", "score", 15, 0.5)
    assert pipeline.snapshot("u1", 12) == {"age": 30}
    assert pipeline.snapshot("u1", 20) == {"age": 31, "score": 0.5}
    assert pipeline.snapshot("missing", 20) == {}


def test_schema_and_cutoff_validation():
    pipeline = FeaturePipeline({"count": int})
    with pytest.raises(ValueError):
        pipeline.ingest("u", "unknown", 1, 1)
    with pytest.raises(TypeError):
        pipeline.ingest("u", "count", 1, "1")
    with pytest.raises(TypeError):
        pipeline.ingest("u", "count", 1, True)
    with pytest.raises(ValueError):
        pipeline.snapshot("u", -1)


def test_snapshot_is_copy_isolated():
    pipeline = FeaturePipeline({"profile": dict})
    pipeline.ingest("u", "profile", 1, {"tier": "free"})
    snapshot = pipeline.snapshot("u", 1)
    snapshot["profile"]["tier"] = "paid"
    assert pipeline.snapshot("u", 1)["profile"] == {"tier": "free"}
