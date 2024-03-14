from __future__ import annotations
from typing import *
if TYPE_CHECKING:
    pass

import sys
import time
from pathlib import Path

import pygame as pyg

from simulacrum_engine.utils.io_utils import read_json
from simulacrum_engine.config import InputConfig


class InputState:

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


class Input:

    def __init__(self, config: InputConfig) -> None:
        self.state = "main"
        self.text_buffer = None

        self.input = {}
        for value in config.model_dump().values():
            self.input[pyg.key.key_code(value)] = InputState()

        self.repeat_rate = 0.2
        self.repeat_delay = 0.5
        self.repeat_times = {key: time.time() for key in config.model_dump()}
        self.shift = False

    def pressed(self, key: str) -> bool:
        return self.input[key].just_pressed if key in self.input else False

    def holding(self, key: str) -> bool:
        return self.input[key].pressed if key in self.input else False

    def released(self, key: str) -> bool:
        return self.input[key].just_released if key in self.input else False

    def movement(self):
        pass

    def update(self) -> None:
        for state in self.input.values():
            state.update()

        for event in pyg.event.get():
            if event.type == pyg.QUIT:
                pyg.quit()
                sys.exit()
