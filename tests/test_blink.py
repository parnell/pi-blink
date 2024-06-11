import pytest

from pi_blink.blink import Blink, EventPriority, listener


# Define some dummy event classes
class EventA:
    def __init__(self):
        self.order = []


class EventB:
    def __init__(self):
        self.order = []


class EventC:
    def __init__(self):
        self.order = []


class StaticEvent:
    def __init__(self):
        self.order = []


class CustomEventForDelete:
    def __init__(self):
        self.order = []


class CustomEventForChangeOrder:
    def __init__(self):
        self.order = []


# Dummy listener functions
@listener(EventA)
def handle_event_a1(event):
    event.order.append("a1")


@listener(EventA)
def handle_event_a2(event):
    event.order.append("a2")


@listener(EventB)
def handle_event_b1(event):
    event.order.append("b1")


@listener(EventB)
def handle_event_b2(event):
    event.order.append("b2")


@listener(EventC)
def handle_event_c1(event):
    event.order.append("c1")


@listener(EventC)
def handle_event_c2(event):
    event.order.append("c2")


class ClassWithStaticMethods:

    @staticmethod
    @listener(StaticEvent)
    def s1(event):
        event.order.append("s1")

    @staticmethod
    @listener(StaticEvent)
    def s2(event):
        event.order.append("s2")


@listener(CustomEventForChangeOrder)
def custom_event_for_change_order_handler_1(event):
    event.order.append("custom_event_for_change_order_handler_1")


@listener(CustomEventForChangeOrder)
def custom_event_for_change_order_handler_2(event):
    event.order.append("custom_event_for_change_order_handler_2")


@listener(CustomEventForDelete)
def custom_event_for_delete_handler_1(event):
    event.order.append("custom_event_for_delete_handler_1")


@listener(CustomEventForDelete)
def custom_event_for_delete_handler_2(event):
    event.order.append("custom_event_for_delete_handler_2")


def test_static_method_listener():
    event = StaticEvent()
    Blink.send(event)
    assert event.order == ["s1", "s2"]


def test_in_method_class_and_listener():
    class InMethodEvent:
        def __init__(self):
            self.order = []

    @listener(InMethodEvent)
    def in_method_listener_1(event):
        event.order.append("in_method_listener_1")

    @listener(InMethodEvent)
    def in_method_listener_2(event):
        event.order.append("in_method_listener_2")

    event = InMethodEvent()
    Blink.send(event)
    assert event.order == ["in_method_listener_1", "in_method_listener_2"]


class MethodEvent:
    def __init__(self):
        self.order = []


def test_in_method_listener():
    @listener(MethodEvent)
    def in_method_listener_1(event):
        event.order.append("in_method_listener_1")

    @listener(MethodEvent)
    def in_method_listener_2(event):
        event.order.append("in_method_listener_2")

    event = MethodEvent()
    Blink.send(event)
    assert event.order == ["in_method_listener_1", "in_method_listener_2"]


# Test multiple event types
def test_multiple_event_types():
    event_a = EventA()
    event_b = EventB()
    event_c = EventC()

    Blink.send(event_a)
    Blink.send(event_b)
    Blink.send(event_c)

    assert "a1" in event_a.order
    assert "a2" in event_a.order
    assert "b1" in event_b.order
    assert "b2" in event_b.order
    assert "c1" in event_c.order
    assert "c2" in event_c.order


# Test event processing order
def test_event_order():
    event_a = EventA()
    event_b = EventB()
    event_c = EventC()

    Blink.send(event_a)
    Blink.send(event_b)
    Blink.send(event_c)

    assert event_a.order == ["a1", "a2"]
    assert event_b.order == ["b1", "b2"]
    assert event_c.order == ["c1", "c2"]


def test_change_listener_priority():
    event = CustomEventForChangeOrder()

    # Change priority of custom_event_handler_2 to EARLIEST
    Blink.change_listener_priority(
        CustomEventForChangeOrder,
        custom_event_for_change_order_handler_2,
        EventPriority.EARLIEST,
    )
    Blink.send(event)
    n1 = "custom_event_for_change_order_handler_{i}".format(i=1)
    n2 = "custom_event_for_change_order_handler_{i}".format(i=2)
    assert event.order == [n2, n1]
    # Reset priority
    Blink.change_listener_priority(
        CustomEventForChangeOrder,
        custom_event_for_change_order_handler_2,
        EventPriority.LATEST,
    )
    event = CustomEventForChangeOrder()

    Blink.send(event)

    assert event.order == [n1, n2]


def test_delete_listener():
    event = CustomEventForDelete()

    # Delete custom_event_handler_1 listener
    Blink.delete_listener(CustomEventForDelete, custom_event_for_delete_handler_1)
    Blink.send(event)

    assert event.order == ["custom_event_for_delete_handler_2"]


if __name__ == "__main__":
    pytest.main([__file__])
