from pi_blink import blink


class MathEvent:
    def __init__(self, value: int):
        self.value = value


@blink.listener(MathEvent)
def add3(event: MathEvent):
    event.value += 3


@blink.listener(MathEvent)
def multiply2(event: MathEvent):
    event.value *= 2


if __name__ == "__main__":
    e = MathEvent(1)
    blink.send(e)
    assert e.value == 8
