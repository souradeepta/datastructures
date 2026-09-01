"""A small, in-memory checkout model for system-design practice.

The model focuses on validating a cart, reserving every item atomically, and
creating an immutable order snapshot. It does not model payments, persistence,
concurrency, or a real product catalog.
"""

from __future__ import annotations

from dataclasses import dataclass
from types import MappingProxyType
from typing import Dict, Mapping, Optional


class Cart:
    """A minimal mutable product-to-quantity cart."""

    def __init__(self) -> None:
        self.items: Dict[str, int] = {}


@dataclass(frozen=True)
class Order:
    """An immutable snapshot of a confirmed checkout."""

    user: object
    items: Mapping[str, int]
    status: str = "confirmed"

    def __init__(self, user: object, items: Mapping[str, int]) -> None:
        object.__setattr__(self, "user", user)
        object.__setattr__(self, "items", MappingProxyType(dict(items)))
        object.__setattr__(self, "status", "confirmed")


class Inventory:
    """In-memory stock ledger with all-or-nothing reservations."""

    def __init__(self, stock: Optional[Mapping[str, int]] = None) -> None:
        self.stock: Dict[str, int] = dict(stock or {})
        if any(not self._valid_quantity(quantity) for quantity in self.stock.values()):
            raise ValueError("stock quantities must be non-negative integers")

    @staticmethod
    def _valid_quantity(quantity: object) -> bool:
        return isinstance(quantity, int) and not isinstance(quantity, bool) and quantity >= 0

    def add_stock(self, product: str, quantity: int) -> None:
        """Add non-negative stock for *product*."""
        if not self._valid_quantity(quantity):
            raise ValueError("stock quantity must be a non-negative integer")
        self.stock[product] = self.stock.get(product, 0) + quantity

    def available(self, product: str) -> int:
        """Return available stock, or zero for an unknown product."""
        return self.stock.get(product, 0)

    def reserve(self, product: str, quantity: int) -> bool:
        """Reserve stock if available; leave the ledger unchanged on failure."""
        if not self._valid_quantity(quantity) or quantity == 0:
            return False
        if product not in self.stock or self.stock[product] < quantity:
            return False
        self.stock[product] -= quantity
        return True

    def release(self, product: str, quantity: int) -> None:
        """Return reserved stock and reject invalid or unknown releases."""
        if not self._valid_quantity(quantity) or quantity == 0:
            raise ValueError("release quantity must be a positive integer")
        if product not in self.stock:
            raise KeyError(product)
        self.stock[product] += quantity


class ECommerce:
    """Educational checkout service backed by one in-memory inventory."""

    def __init__(self, inventory: Optional[Inventory] = None) -> None:
        self.cart = Cart()
        self.inv = inventory or Inventory()
        self.orders: list[Order] = []

    def checkout(self, user: object, items: Mapping[str, int]) -> Optional[Order]:
        """Reserve *items* atomically and return a confirmed immutable order.

        Invalid cart shapes or quantities raise ``ValueError`` before state is
        changed. Unknown products and insufficient stock return ``None`` and
        also leave stock and the order list unchanged.
        """
        if not isinstance(items, Mapping) or not items:
            raise ValueError("items must be a non-empty product-to-quantity mapping")
        requested = dict(items)
        if any(
            not isinstance(product, str)
            or not isinstance(quantity, int)
            or isinstance(quantity, bool)
            or quantity <= 0
            for product, quantity in requested.items()
        ):
            raise ValueError("each product quantity must be a positive integer")

        if any(
            product not in self.inv.stock or self.inv.stock[product] < quantity
            for product, quantity in requested.items()
        ):
            return None

        for product, quantity in requested.items():
            self.inv.stock[product] -= quantity
        order = Order(user, requested)
        self.orders.append(order)
        return order


if __name__ == "__main__":
    shop = ECommerce(Inventory({"book": 2}))
    print(shop.checkout("demo-user", {"book": 1}))
