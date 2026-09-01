import pytest

from python.system_design.ecommerce import ECommerce, Inventory


def test_checkout_reserves_all_items_and_returns_immutable_snapshot():
    shop = ECommerce(Inventory({"book": 3, "pen": 5}))
    items = {"book": 1, "pen": 2}

    order = shop.checkout("alice", items)

    assert order is not None
    assert order.user == "alice"
    assert order.items == {"book": 1, "pen": 2}
    assert order.status == "confirmed"
    assert shop.inv.stock == {"book": 2, "pen": 3}
    items["book"] = 99
    assert order.items["book"] == 1
    with pytest.raises(TypeError):
        order.items["book"] = 2


def test_failed_checkout_is_atomic_for_later_item_and_unknown_product():
    shop = ECommerce(Inventory({"book": 2, "pen": 1}))
    original = dict(shop.inv.stock)

    assert shop.checkout("alice", {"book": 2, "pen": 2}) is None
    assert shop.checkout("alice", {"book": 1, "pencil": 1}) is None
    assert shop.inv.stock == original
    assert shop.orders == []


@pytest.mark.parametrize("items", [{}, {"book": 0}, {"book": -1}, {"book": 1.5}])
def test_invalid_checkout_input_has_no_side_effect(items):
    shop = ECommerce(Inventory({"book": 2}))
    with pytest.raises(ValueError):
        shop.checkout("alice", items)
    assert shop.inv.stock == {"book": 2}
    assert shop.orders == []


def test_inventory_reserve_and_release_validate_stock():
    inventory = Inventory({"book": 2})
    assert inventory.reserve("book", 2)
    assert inventory.available("book") == 0
    assert not inventory.reserve("book", 1)
    assert not inventory.reserve("missing", 1)
    inventory.release("book", 2)
    assert inventory.available("book") == 2
    with pytest.raises(KeyError):
        inventory.release("missing", 1)
    with pytest.raises(ValueError):
        inventory.release("book", 0)
