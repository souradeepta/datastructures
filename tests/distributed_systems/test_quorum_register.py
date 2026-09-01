import pytest

from python.distributed_systems.quorum_register import QuorumRegister


def test_write_read_and_read_repair():
    register = QuorumRegister(["a", "b", "c"], read_quorum=2, write_quorum=2)
    register.write("user", {"name": "Ada"})
    register.set_replica_available("a", False)
    assert register.read("user").value == {"name": "Ada"}
    register.set_replica_available("a", True)
    assert register.replica_value("c", "user").value == {"name": "Ada"}


def test_read_repairs_stale_replica_in_contacted_set():
    register = QuorumRegister(["a", "b", "c", "d", "e"], 3, 3)
    register.write("k", "old")
    register.set_replica_available("a", False)
    register.set_replica_available("b", False)
    register.write("k", "new")  # c, d, and e receive the newer value
    register.set_replica_available("a", True)
    register.set_replica_available("c", False)
    assert register.read("k").value == "new"
    assert register.replica_value("a", "k").value == "new"


def test_unavailable_quorums_fail_without_partial_write():
    register = QuorumRegister([1, 2, 3], 2, 2)
    register.set_replica_available(1, False)
    register.set_replica_available(2, False)
    with pytest.raises(RuntimeError, match="write quorum"):
        register.write("k", 1)
    with pytest.raises(RuntimeError, match="read quorum"):
        register.read("k")


def test_quorum_intersection_is_required():
    with pytest.raises(ValueError, match="greater than N"):
        QuorumRegister(["a", "b", "c"], read_quorum=1, write_quorum=2)


def test_reads_and_writes_isolate_mutable_values():
    register = QuorumRegister(["a", "b", "c"], 2, 2)
    payload = {"items": [1]}
    register.write("k", payload)
    payload["items"].append(2)
    result = register.read("k")
    result.value["items"].append(3)
    assert register.read("k").value == {"items": [1]}
