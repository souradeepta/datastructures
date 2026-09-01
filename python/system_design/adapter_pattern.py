"""Adapter Pattern - Interface compatibility layer"""

from abc import ABC, abstractmethod


class Payment(ABC):
    """Target payment interface"""

    @abstractmethod
    def pay(self, amount: float) -> bool:
        """Process a payment and report whether it succeeded."""
        raise NotImplementedError


class LegacyPaymentSystem:
    """Legacy payment system with different interface"""

    def process_payment(self, amount_cents: int) -> bool:
        """Legacy system takes cents, returns success/fail"""
        print(f"Legacy system processing ${amount_cents / 100:.2f}")
        return True


class PaymentAdapter(Payment):
    """Adapter to make legacy system compatible"""

    def __init__(self, legacy_system: LegacyPaymentSystem):
        self.legacy_system = legacy_system

    def pay(self, amount: float) -> bool:
        """Translate new interface to legacy interface"""
        amount_cents = int(amount * 100)
        return self.legacy_system.process_payment(amount_cents)


class ModernPaymentGateway(Payment):
    """Modern payment system"""

    def pay(self, amount: float) -> bool:
        """Process a payment through the modern gateway."""
        print(f"Modern gateway processing ${amount:.2f}")
        return True


class ShoppingCart:
    """Shopping cart using payment interface"""

    def __init__(self, payment: Payment):
        self.payment = payment
        self.total = 0.0

    def add_item(self, price: float):
        """Add an item price to the running cart total."""
        self.total += price

    def checkout(self) -> bool:
        """Charge the cart total through the configured payment service."""
        return self.payment.pay(self.total)


if __name__ == "__main__":
    cart1 = ShoppingCart(ModernPaymentGateway())
    cart1.add_item(10.50)
    cart1.add_item(25.75)
    print("=== Modern Gateway ===")
    cart1.checkout()

    print()

    legacy = LegacyPaymentSystem()
    adapter = PaymentAdapter(legacy)
    cart2 = ShoppingCart(adapter)
    cart2.add_item(15.99)
    cart2.add_item(8.50)
    print("=== Legacy System (via Adapter) ===")
    cart2.checkout()
