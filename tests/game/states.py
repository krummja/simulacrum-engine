from __future__ import annotations
from typing import *
if TYPE_CHECKING:
    pass

import logging
from devtools import debug
from transitions.extensions import HierarchicalMachine
from transitions.extensions.nesting import NestedState


logging.basicConfig(level=logging.INFO)

NestedState.separator = '+'


class State(TypedDict):
    name: str
    children: NotRequired[list[State]]
    parallel: NotRequired[list[State]]


states: list[State] = [
    State(name="idle"),
    State(name="moving", children=[
        State(name="up"),
        State(name="right"),
        State(name="down"),
        State(name="left"),
    ]),
    State(name="jumping"),
    State(name="falling"),
]
