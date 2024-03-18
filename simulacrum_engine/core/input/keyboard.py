from __future__ import annotations
from typing import *
if TYPE_CHECKING:
    from simulacrum_engine.core.config import InputConfig

import time
import pygame as pyg

from devtools import debug

from .input_method import InputMethod


class KeyState:

    def __init__(self) -> None:
        self.pressed = False
        self.just_pressed = False
        self.just_released = False
        self.held_since = 0

    def update(self) -> None:
        self.just_pressed = False
        self.just_released = False

    def press(self) -> None:
        self.pressed = True
        self.just_pressed = True
        self.held_since = time.time()

    def unpress(self) -> None:
        self.pressed = False
        self.just_released = True


class Keyboard(InputMethod):

    def setup(self, config: InputConfig) -> None:
        self.text_buffer = None
        self.config = config.model_dump().items()
        self.states = {value: KeyState() for _, value in self.config}

        self.repeat_rate = 0.2
        self.repeat_delay = 0.5
        self.repeat_times = {key: time.time() for key in config.model_dump()}
        self.shift = False

    def pressed(self, key: str) -> bool:
        return (
            self.states[key].just_pressed
            if key in self.states
            else False
        )

    def holding(self, key: str) -> bool:
        return (
            self.states[key].pressed
            if key in self.states
            else False
        )

    def released(self, key: str) -> bool:
        return (
            self.states[key].just_released
            if key in self.states
            else False
        )

    def movement(self):
        pass

    def update(self) -> None:
        for state in self.states.values():
            state.update()
