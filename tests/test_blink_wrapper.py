import pytest

from pi_blink.blink import blink


# Define some dummy event classes
class EventA:
    def __init__(self):
        self.order = []

    def __repr__(self):
        return f"<EventA order={self.order}>"


# Dummy listener functions
@blink.listener(EventA)
def handle_event_a1(event):
    event.order.append("a1")


@blink.listener(EventA)
def handle_event_a2(event):
    event.order.append("a2")


# Test event processing order
def test_event_order():
    event_a = EventA()

    blink.send(event_a)

    assert event_a.order == ["a1", "a2"]


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
