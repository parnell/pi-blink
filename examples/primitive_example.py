from pi_blink import blink


@blink.listener("zot")
def handle_event_a1(event):
    print(f"handle_event_a1: {event}")


@blink.listener("zot")
def handle_event_a2(event):
    print(f"handle_event_a2: {event}")


if __name__ == "__main__":
    blink.send("zot")
