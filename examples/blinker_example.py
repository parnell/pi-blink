import asyncio

from blinker import signal

started = signal('round-started')
def each(round):
    print(f"Round {round}")

started.connect(each)

def round_two(round):
    print("This is round two.")

started.connect(round_two, sender=2)

def main():
    for round in range(1, 4):
        started.send(round)


if __name__ ==  '__main__':
    main()