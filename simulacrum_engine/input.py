from __future__ import annotations
from typing import *
if TYPE_CHECKING:
    pass

import sys
import time
from pathlib import Path

import pygame as pyg

from simulacrum_engine.io_utils import read_json


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

    def __init__(self, config_path: str | Path | None = None) -> None:
        self.state = "main"
        self.text_buffer = None

        self.config = read_json(config_path) if config_path else {}
        self.input = {key: InputState() for key in self.config}

        self.repeat_rate = 0.2
        self.repeat_delay = 0.5
        self.repeat_times = {key: time.time() for key in self.config}
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
