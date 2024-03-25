from __future__ import annotations
from typing import *
if TYPE_CHECKING:
    pass

from enum import StrEnum

from statemachine import StateMachine
from statemachine import State
from statemachine.states import States


class PowerSwitch(StateMachine):

    power_off = State(initial=True)
    power_on = State()

    turn_on = power_off.to(power_on)
    turn_off = power_on.to(power_off)


if __name__ == '__main__':
    from devtools import debug

    switch = PowerSwitch()
    switch.turn_on()
    debug(switch)

    switch.turn_off()
    debug(switch)
