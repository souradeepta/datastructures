import pytest

from python.system_design.adapter_pattern import (
    LegacyPaymentSystem,
    PaymentAdapter,
    ShoppingCart as AdapterCart,
)
from python.system_design.decorator_pattern import (
    MilkDecorator,
    SimpleCoffee,
    SugarDecorator,
)
from python.system_design.factory_pattern import (
    DatabaseFactory,
    MongoDBDatabase,
    MySQLDatabase,
    PostgreSQLDatabase,
)
from python.system_design.observer_pattern import Button, DisplayObserver
from python.system_design.strategy_pattern import (
    CreditCardPayment,
    PayPalPayment,
    ShoppingCart as StrategyCart,
)


class RecordingLegacyPayment(LegacyPaymentSystem):
    def __init__(self):
        self.amount_cents = None

    def process_payment(self, amount_cents: int) -> bool:
        self.amount_cents = amount_cents
        return True


def test_adapter_translates_dollars_to_legacy_cents():
    legacy = RecordingLegacyPayment()
    cart = AdapterCart(PaymentAdapter(legacy))
    cart.add_item(12.34)

    assert cart.checkout()
    assert legacy.amount_cents == 1234


def test_decorator_composes_cost_and_description():
    coffee = SugarDecorator(MilkDecorator(SimpleCoffee()))

    assert coffee.get_cost() == pytest.approx(2.75)
    assert coffee.get_description() == "Simple coffee, milk, sugar"


@pytest.mark.parametrize(
    ("db_type", "expected_type"),
    [
        ("mysql", MySQLDatabase),
        ("postgresql", PostgreSQLDatabase),
        ("mongodb", MongoDBDatabase),
    ],
)
def test_factory_creates_requested_database(db_type, expected_type):
    assert isinstance(DatabaseFactory.create_database(db_type), expected_type)


def test_factory_rejects_unsupported_database_type():
    with pytest.raises(ValueError, match="Unknown database type"):
        DatabaseFactory.create_database("sqlite")


def test_observer_notifies_and_detach_stops_notifications():
    button = Button()
    display = DisplayObserver()
    button.attach(display)
    button.attach(display)  # attaching twice must not duplicate notifications

    button.press()
    assert display.status == "pressed"
    button.detach(display)
    button.release()
    assert display.status == "pressed"


@pytest.mark.parametrize(
    "strategy",
    [CreditCardPayment("1111-2222", "123"), PayPalPayment("user@example.com")],
)
def test_strategy_cart_uses_selected_payment_strategy(strategy):
    cart = StrategyCart()
    cart.add_item(10.0)
    cart.set_payment_strategy(strategy)

    assert cart.checkout()


def test_strategy_cart_without_strategy_fails(capsys):
    assert not StrategyCart().checkout()
    assert "No payment strategy selected" in capsys.readouterr().out
