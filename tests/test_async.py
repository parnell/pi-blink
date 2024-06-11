import asyncio
from dataclasses import dataclass

import pytest

from pi_blink.blink import Blink, alistener


# Define a test event class
@dataclass
class SampleEvent:
    value: int
    cancel: bool = False


# Define an async listener
@alistener(SampleEvent)
async def async_listener(event: SampleEvent):
    await asyncio.sleep(0.8)
    event.value += 3


@alistener(SampleEvent)
async def async_listener2(event: SampleEvent):
    event.value *= 2


@alistener(SampleEvent)
async def sync_listener3(event: SampleEvent):
    event.value *= 2


@pytest.mark.asyncio
async def test_async_sending():
    event = SampleEvent(value=1)
    # Send event using async send
    await Blink.asend(event)

    # Check the results after async listeners have run
    assert event.value == 16


## TODO Implement cancel
# @pytest.mark.asyncio
# async def test_async_cancel():
#     event = SampleEvent(value=1)
#     # Send event using async send
#     await Blink.asend(event)

#     # Check the results after async listeners have run
#     assert event.value == 16


if __name__ == "__main__":
    testmethod = ""
    pytest.main([__file__, "-k", testmethod])
