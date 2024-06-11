import pytest

from pi_blink.blink import Blink, listener
from pi_blink.events import StopEvent


class EventA:
    def __init__(self):
        self.order = []

    def __repr__(self):
        return f"<EventA order={self.order}>"


@listener(EventA)
def handle_event_a1(event):
    event.order.append("a1")
    return StopEvent()


@listener(EventA)
def handle_event_a2(event):
    event.order.append("a2")
    return event


def test_is_stopped():
    event = EventA()
    Blink.send(event)
    assert event.order == ["a1"]


class EventB:
    def __init__(self):
        self.order = []

    def __repr__(self):
        return f"<EventB order={self.order}>"


@listener(EventB)
def handle_event_b1(event):
    event.order.append("b1")
    raise ValueError("Error in handle_event_b1")


@listener(EventB)
def handle_event_b2(event):
    event.order.append("b2")


def test_is_raised():
    event = EventB()
    ## this should raise an error
    with pytest.raises(ValueError):
        Blink.send(event)

    ## Event should still have the order of the 
    ## first listener as it's added before the error
    assert event.order == ["b1"]
    

def test_is_safe():
    event = EventB()
    ## this should raise an error
    result = Blink.send_safe(event)

    ## Event should still have the order of the 
    ## first listener as it's added before the error
    assert event.order == ["b1", "b2"]
    assert len(result.listeners) == len(result.results) == 1
    assert result.errors[0].args[0] == "Error in handle_event_b1"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
