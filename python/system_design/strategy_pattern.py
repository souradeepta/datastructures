"""Strategy Pattern - Runtime algorithm switching"""

from abc import ABC, abstractmethod


class PaymentStrategy(ABC):
    """Payment strategy interface"""

    @abstractmethod
    def pay(self, amount: float) -> bool:
        """Process a payment using the selected strategy."""
        raise NotImplementedError


class CreditCardPayment(PaymentStrategy):
    """Credit card payment strategy"""

    def __init__(self, card_number: str, cvv: str):
        self.card_number = card_number
        self.cvv = cvv

    def pay(self, amount: float) -> bool:
        print(f"Processing credit card payment of ${amount}")
        print(f"  Card: {self.card_number[-4:]}")
        return True


class PayPalPayment(PaymentStrategy):
    """PayPal payment strategy"""

    def __init__(self, email: str):
        self.email = email

    def pay(self, amount: float) -> bool:
        print(f"Processing PayPal payment of ${amount}")
        print(f"  Email: {self.email}")
        return True


class BitcoinPayment(PaymentStrategy):
    """Bitcoin payment strategy"""

    def __init__(self, address: str):
        self.address = address

    def pay(self, amount: float) -> bool:
        print(f"Processing Bitcoin payment of ${amount}")
        print(f"  Address: {self.address}")
        return True


class ShoppingCart:
    """Context that uses payment strategy"""

    def __init__(self):
        self.items = []
        self.payment_strategy = None

    def add_item(self, price: float):
        self.items.append(price)

    def set_payment_strategy(self, strategy: PaymentStrategy):
        """Select the payment strategy used at checkout."""
        self.payment_strategy = strategy

    def checkout(self) -> bool:
        total = sum(self.items)
        if not self.payment_strategy:
            print("No payment strategy selected")
            return False
        return self.payment_strategy.pay(total)


if __name__ == "__main__":
    cart = ShoppingCart()
    cart.add_item(29.99)
    cart.add_item(15.50)

    print("=== Credit Card ===")
    cart.set_payment_strategy(CreditCardPayment("1234-5678-9012-3456", "123"))
    cart.checkout()

    cart2 = ShoppingCart()
    cart2.add_item(99.99)

    print("\n=== PayPal ===")
    cart2.set_payment_strategy(PayPalPayment("user@example.com"))
    cart2.checkout()

    print("\n=== Bitcoin ===")
    cart2.set_payment_strategy(BitcoinPayment("1A1z7agoat2LWSR2k4SSQwDjggyziQS91g"))
    cart2.checkout()
