from pi_blink import blink

class EventA:
    def __init__(self):
        self.order = []


@blink.listener(EventA)
def handle_event_a1(event : EventA):
    event.order.append("a1")


@blink.listener(EventA)
def handle_event_a2(event : EventA):
    event.order.append("a2")

if __name__ == "__main__":
    event_a = EventA()
    blink.send(event_a)
    assert event_a.order == ["a1", "a2"]
