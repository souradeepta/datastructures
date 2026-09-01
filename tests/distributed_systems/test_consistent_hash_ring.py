from python.distributed_systems.consistent_hash_ring import ConsistentHashRing


def test_routing_is_deterministic_and_wraps():
    first = ConsistentHashRing(["a", "b", "c"], virtual_nodes=20)
    second = ConsistentHashRing(["c", "a", "b"], virtual_nodes=20)
    keys = ["alpha", "beta", "wraparound", "42"]
    assert [first.get_node(key) for key in keys] == [second.get_node(key) for key in keys]
    assert first.get_node("alpha") in first.nodes


def test_replica_selection_is_unique_and_bounded():
    ring = ConsistentHashRing(["a", "b", "c"], virtual_nodes=10)
    replicas = ring.get_replicas("key", 10)
    assert len(replicas) == 3
    assert len(set(replicas)) == len(replicas)


def test_add_remove_and_migration_plan():
    ring = ConsistentHashRing(["a", "b", "c"], virtual_nodes=50)
    keys = [f"key-{index}" for index in range(500)]
    old = {key: ring.get_node(key) for key in keys}
    ring.add_node("d")
    plan = ring.migration_plan(keys, old)
    moved = [key for key, (before, after) in plan.items() if before != after]
    assert 0 < len(moved) < len(keys)
    ring.remove_node("d")
    assert all(ring.get_node(key) in {"a", "b", "c"} for key in keys)
