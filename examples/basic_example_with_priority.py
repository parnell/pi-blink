from pi_blink import blink, EventPriority

class EventA:
    def __init__(self):
        self.order = []


@blink.listener(EventA)
def handle_event_a1(event : EventA):
    event.order.append("a1")


@blink.listener(EventA, EventPriority.EARLY)
def handle_event_a2(event : EventA):
    event.order.append("a2")

if __name__ == "__main__":
    event_a = EventA()
    blink.send(event_a)
    print(event_a.order)
    assert event_a.order == ["a2", "a1"]
