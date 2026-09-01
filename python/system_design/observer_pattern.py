"""Observer Pattern - Event publishing and subscription"""

class Observer:
    """Observer interface"""

    def update(self, subject):
        """React to a change in the observed subject."""
        raise NotImplementedError


class Subject:
    """Observable subject"""

    def __init__(self):
        self._observers = []

    def attach(self, observer: Observer):
        """Attach observer"""
        if observer not in self._observers:
            self._observers.append(observer)

    def detach(self, observer: Observer):
        """Detach observer"""
        if observer in self._observers:
            self._observers.remove(observer)

    def notify(self):
        """Notify all observers"""
        for observer in self._observers:
            observer.update(self)


class Button(Subject):
    """Concrete subject - Button"""

    def __init__(self):
        super().__init__()
        self._is_pressed = False

    def press(self):
        """Button pressed"""
        self._is_pressed = True
        self.notify()

    def release(self):
        """Button released"""
        self._is_pressed = False
        self.notify()

    @property
    def is_pressed(self):
        """Return the current button state."""
        return self._is_pressed


class LogObserver(Observer):
    """Concrete observer - Log events"""

    def __init__(self, name: str):
        self.name = name

    def update(self, subject: Button):
        print(f"[{self.name}] Button is {'pressed' if subject.is_pressed else 'released'}")


class DisplayObserver(Observer):
    """Concrete observer - Display status"""

    def __init__(self):
        self.status = "released"

    def update(self, subject: Button):
        self.status = "pressed" if subject.is_pressed else "released"
        print(f"[Display] Current status: {self.status}")


if __name__ == "__main__":
    button = Button()

    log_obs = LogObserver("Logger")
    display_obs = DisplayObserver()

    button.attach(log_obs)
    button.attach(display_obs)

    print("=== Pressing button ===")
    button.press()

    print("\n=== Releasing button ===")
    button.release()

    print("\n=== Detaching logger ===")
    button.detach(log_obs)
    button.press()
