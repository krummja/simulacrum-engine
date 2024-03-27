from __future__ import annotations
from typing import *
from dataclasses import dataclass, field
import pecs_framework as pecs

from transitions.extensions import HierarchicalMachine
from transitions.extensions.nesting import NestedState
from transitions.extensions.nesting import NestedTransition


class StateControl(pecs.Component):

    def __init__(
        self,
        states: list[NestedState],
        state_model: Any = None,
        initial: NestedState | None = None,
        transitions: list[NestedTransition] | None = None,
    ) -> None:
        self.states = states
        self.state_model = state_model
        self.initial = initial
        self.transitions = transitions

        NestedState.separator = "+"

        self.machine = HierarchicalMachine(
            model=self.state_model,
            states=self.states if self.states else [],
            transitions=self.transitions if self.transitions else [],
            initial=self.initial,
        )

    def on_request_state(self, evt: pecs.EntityEvent) -> pecs.EntityEvent:
        state_name = evt.data.state_name
        self.state_model.to(state_name)
        return evt
