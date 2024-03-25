from __future__ import annotations
from typing import *
from dataclasses import dataclass
import pecs_framework as pecs

from statemachine import StateMachine
from statemachine.states import States


class State(pecs.Component):

    def __init__(self) -> None:
        self._machine = StateMachine()
