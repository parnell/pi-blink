from pi_blink.blink import Blink, listener


class RoundStarted:
    def __init__(self, round):
        self.round = round


@listener(RoundStarted)
def each(round_started):
    print(f"Round {round_started.round}")


## TODO currently sender is not implemented
@listener(RoundStarted, sender=2)
def round_two(round_started):
    print("This is round two.")


for round in range(1, 4):
    Blink.send(RoundStarted(round), sender=round)
