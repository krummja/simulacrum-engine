from __future__ import annotations
from typing import *
if TYPE_CHECKING:
    pass

from statemachine import StateMachine, State


class TrafficLight(StateMachine):

    green = State(initial=True)
    yellow = State()
    red = State()

    cycle = (green.to(yellow) | yellow.to(red) | red.to(green))

    def before_cycle(self, event: str, source: State, target: State, msg: str = ""):
        message = ". " + msg if msg else ""
        return f"Running {event} from {source.id} to {target.id}{message}"

    def on_enter_red(self):
        print("Stop!")

    def on_exit_red(self):
        print("Go!")


if __name__ == '__main__':
    sm = TrafficLight()
    sm.send("cycle")
    print(sm.current_state.id)

    sm.cycle()
    print(sm.current_state)
