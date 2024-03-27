from __future__ import annotations
from typing import *
if TYPE_CHECKING:
    pass

from transitions import State, Transition
from transitions.core import TransitionConfig
from transitions.extensions import HierarchicalMachine


states = [
    "standing",
    "walking",
    {
        "name": "caffeinated",
        "children": [
            "dithering",
            "running",
        ]
    }
]

transitions = [
    ["walk", "standing", "walking"],
    ["stop", "walking", "standing"],
    ["drink", "*", "caffeinated"],
    ["walk", ["caffeinated", "caffeinated_dithering"], "caffeinated_running"],
    ["relax", "caffeinated", "standing"],
]

machine = HierarchicalMachine(
    states=states,
    transitions=transitions,
    initial="standing",
    ignore_invalid_triggers=True,
)

machine.walk()
machine.stop()
machine.drink()
print(machine.state)

machine.stop()
print(machine.state)

machine.relax()
print(machine.state)
