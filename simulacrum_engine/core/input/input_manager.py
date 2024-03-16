from __future__ import annotations
from typing import *
if TYPE_CHECKING:
    pass

import pygame as pyg

from simulacrum_engine.core.logger import log_boot
from simulacrum_engine.core.component import EngineComponent
from simulacrum_engine.core.events import Events
from .keyboard import Keyboard
from .mouse import Mouse


class InputManager(EngineComponent):

    def boot(self) -> bool:
        self.config = self.engine.config.input
        self.keyboard = Keyboard(self)
        self.mouse = Mouse(self)

        self.emitter.on(Events.POST_UPDATE, self.cycle)
        return True

    def ready(self) -> None:
        pass

    def teardown(self) -> None:
        pass

    def cycle(self) -> None:
        self.keyboard.update()

        for event in pyg.event.get():
            if event.type == pyg.QUIT:
                self.engine.teardown()
