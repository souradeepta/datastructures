"""Decorator Pattern - Dynamic behavior extension"""

from abc import ABC, abstractmethod


class Coffee(ABC):
    """Coffee interface"""

    @abstractmethod
    def get_cost(self) -> float:
        """Return the current coffee cost."""
        raise NotImplementedError

    @abstractmethod
    def get_description(self) -> str:
        """Return a human-readable coffee description."""
        raise NotImplementedError


class SimpleCoffee(Coffee):
    """Base coffee"""

    def get_cost(self) -> float:
        return 2.0

    def get_description(self) -> str:
        return "Simple coffee"


class CoffeeDecorator(Coffee):
    """Base decorator for coffee"""

    def __init__(self, coffee: Coffee):
        self.coffee = coffee

    def get_cost(self) -> float:
        return self.coffee.get_cost()

    def get_description(self) -> str:
        return self.coffee.get_description()


class MilkDecorator(CoffeeDecorator):
    """Add milk to coffee"""

    def get_cost(self) -> float:
        return self.coffee.get_cost() + 0.5

    def get_description(self) -> str:
        return self.coffee.get_description() + ", milk"


class SugarDecorator(CoffeeDecorator):
    """Add sugar to coffee"""

    def get_cost(self) -> float:
        return self.coffee.get_cost() + 0.25

    def get_description(self) -> str:
        return self.coffee.get_description() + ", sugar"


class VanillaDecorator(CoffeeDecorator):
    """Add vanilla to coffee"""

    def get_cost(self) -> float:
        return self.coffee.get_cost() + 0.75

    def get_description(self) -> str:
        return self.coffee.get_description() + ", vanilla"


if __name__ == "__main__":
    # Simple coffee
    coffee = SimpleCoffee()
    print(f"{coffee.get_description()}: ${coffee.get_cost()}")

    # Coffee with milk
    coffee = MilkDecorator(SimpleCoffee())
    print(f"{coffee.get_description()}: ${coffee.get_cost()}")

    # Coffee with milk and sugar
    coffee = SugarDecorator(MilkDecorator(SimpleCoffee()))
    print(f"{coffee.get_description()}: ${coffee.get_cost()}")

    # Coffee with all extras
    coffee = VanillaDecorator(SugarDecorator(MilkDecorator(SimpleCoffee())))
    print(f"{coffee.get_description()}: ${coffee.get_cost()}")
