# Event Handling with Blink

Event handling library built on top of [Blinker](https://github.com/pallets-eco/blinker).


## Why use it instead of blink
Pi-Blink is a different pardigm and a different way of handling events. So if Blink makes more sense then you should certainly use it. In the Pi-Blink paradigm events are created which can be listened, and modified, across your application. 

Some other benefits are Priority-Based Event Handling: This script introduces the concept of event priorities, allowing you to specify the order in which event listeners should be executed. This can be useful when you have multiple listeners for the same event and need to control their execution sequence.

## Installation

You can install `pi-blink` via pip:

```bash
pip install pi-blink
```

## Basic Usage
Import
```python
from pi_blink import blink
```

Create an event to listen to. This can be a class or primitive though classes are encouraged.
```python
class MathEvent:
    def __init__(self, value: int):
        self.value = value
```

Set up listeners for the event. 
```python
@blink.listener(MathEvent)
def add3(event: MathEvent):
    event.value += 3


@blink.listener(MathEvent)
def multiply2(event: MathEvent):
    event.value *= 2
```

Create and send an event
```python
e = MathEvent(1)
blink.send(e)
assert e.value == 8
```



## Examples

### Basic Example
```python
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
```

### Basic Example with Priority
```python
from pi_blink import blink

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
    assert event_a.order == ["a2", "a1"]
```

