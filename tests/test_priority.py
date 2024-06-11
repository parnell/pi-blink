from pi_blink import blink, EventPriority
import pytest
class EventA:
    def __init__(self):
        self.order = []


@blink.listener(EventA)
def listen_a(event : EventA):
    event.order.append("a1")


@blink.listener(EventA, priority=EventPriority.EARLY)
def listen_a2(event : EventA):
    event.order.append("a2")

def test_priority_order():
    event_a = EventA()
    blink.send(event_a)
    assert event_a.order == ["a2", "a1"]

if __name__ == "__main__":
    pytest.main([__file__, "-v"])
