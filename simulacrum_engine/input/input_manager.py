from __future__ import annotations
from typing import *
if TYPE_CHECKING:
    pass

import pygame as pyg

from simulacrum_engine.logger import log_boot
from simulacrum_engine.component import EngineComponent
from simulacrum_engine.events import Events
from .keyboard import Keyboard
from .mouse import Mouse


class InputManager(EngineComponent):

    def boot(self) -> bool:
        self.config = self.engine.config.input
        self.keyboard = Keyboard(self)
        self.mouse = Mouse(self)

        self.keyboard.setup(self.config)
        self.mouse.setup(self.config)

        self.emitter.on(Events.POST_UPDATE, self.cycle)
        return True

    def cycle(self) -> None:
        self.keyboard.update()
        self.mouse.update()

        for event in pyg.event.get():
            self.process_event(event)

    def process_event(self, event: pyg.event.Event):
        match event.type:
            case pyg.QUIT:
                self.engine.teardown()

            case pyg.MOUSEBUTTONDOWN:
                pass

            case pyg.MOUSEBUTTONUP:
                pass

            case pyg.KEYDOWN:
                if event.key in [pyg.K_LSHIFT, pyg.K_RSHIFT]:
                    self.keyboard.shift = True

                for mapping in self.config:
                    if event.key == pyg.key.key_code(mapping[1]):
                        self.keyboard.states[mapping[1]].press()

            case pyg.KEYUP:
                for mapping in self.config:
                    if event.key == pyg.key.key_code(mapping[1]):
                        self.keyboard.states[mapping[1]].unpress()

                if event.key in [pyg.K_LSHIFT, pyg.K_RSHIFT]:
                    self.keyboard.shift = False
