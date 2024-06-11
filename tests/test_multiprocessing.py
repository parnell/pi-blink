from concurrent.futures import ThreadPoolExecutor
from multiprocessing import Manager, Process, Queue

import pytest

from pi_blink.blink import Blink, listener


# Define some dummy event classes
class EventA:
    def __init__(self):
        self.order = []
        self.modified_by = []

    def __repr__(self):
        return f"<EventA order={self.order} modified_by={self.modified_by}>"


def worker(queue):
    event = EventA()
    Blink.send(event)
    queue.put(str(event.order))


@listener(EventA)
def handle_event_a1(event):
    print(f"handle_event_a1: {event}")
    event.order.append("a1")
    event.modified_by.append("a1")
    print(f"~handle_event_a1: {event}")
    return event


@listener(EventA)
def handle_event_a2(event):
    print(f"handle_event_a2: {event}")
    event.order.append("a2")
    event.modified_by.append("a2")
    print(f"~handle_event_a2: {event}")
    return event


def test_multiprocessing_listener():
    with Manager() as manager:
        queue = manager.Queue()
        #     # Create and start processes
        processes = [Process(target=worker, args=(queue,)) for _ in range(2)]
        for p in processes:
            p.start()

        for p in processes:
            p.join()

        results = []
        for _ in range(2):
            try:
                result = queue.get(timeout=1)
                results.append(result)
            except Exception as e:
                print(f"Error getting result from queue: {e}")

        # Collect results from the queue
        # Assert that the event was processed by both listeners
        assert len(results) == 2
        for result in results:
            assert result == "['a1', 'a2']"


# Helper function for multiprocessing test
def send_from_process(event_class, queue):
    event = event_class()
    Blink.send(event)
    queue.put(event)


# Test multiprocessing
def test_multiprocessing():
    queue = Queue()
    event_classes = [EventA]

    processes = [
        Process(target=send_from_process, args=(event_class, queue))
        for event_class in event_classes
    ]

    for p in processes:
        p.start()

    for p in processes:
        p.join()

    results = [queue.get() for _ in event_classes]

    for event in results:
        assert event.order == [
            f"{event.__class__.__name__.lower()[-1]}1",
            f"{event.__class__.__name__.lower()[-1]}2",
        ]
        assert event.modified_by == [
            f"{event.__class__.__name__.lower()[-1]}1",
            f"{event.__class__.__name__.lower()[-1]}2",
        ]


# Helper function for threading test
def send_from_thread(event_class):
    event = event_class()
    Blink.send(event)
    return event


# Test threading
def test_threading():
    event_classes = [EventA]

    with ThreadPoolExecutor(max_workers=len(event_classes)) as executor:
        futures = [executor.submit(send_from_thread, event_class) for event_class in event_classes]

    results = [future.result() for future in futures]

    for event in results:
        assert event.order == [
            f"{event.__class__.__name__.lower()[-1]}1",
            f"{event.__class__.__name__.lower()[-1]}2",
        ]
        assert event.modified_by == [
            f"{event.__class__.__name__.lower()[-1]}1",
            f"{event.__class__.__name__.lower()[-1]}2",
        ]


if __name__ == "__main__":
    pytest.main([__file__])
