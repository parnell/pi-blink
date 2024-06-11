from concurrent.futures import ThreadPoolExecutor
from multiprocessing import Manager, Process, Queue

import pytest

from pi_blink.blink import blink


# Define some dummy event classes
class EventA:
    def __init__(self):
        self.order = []
        self.modified_by = []

    def __repr__(self):
        return f"<EventA order={self.order} modified_by={self.modified_by}>"


# Dummy listener functions
@blink.listener(EventA)
def handle_event_a1(event):
    print(f"handle_event_a1: {event}")
    event.order.append("a1")
    event.modified_by.append("a1")
    print(f"~handle_event_a1: {event}")
    return event


@blink.listener(EventA)
def handle_event_a2(event):
    print(f"handle_event_a2: {event}")
    event.order.append("a2")
    event.modified_by.append("a2")
    print(f"~handle_event_a2: {event}")
    return event

# Test event processing order
def test_event_order():
    event_a = EventA()

    blink.send(event_a)

    assert event_a.order == ["a1", "a2"]

if __name__ == "__main__":
    pytest.main([__file__, "-v"])
