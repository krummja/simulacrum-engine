from __future__ import annotations
from typing import *
if TYPE_CHECKING:
    pass

from simulacrum_engine.core.component import EngineComponent
from .keyboard import Keyboard
from .mouse import Mouse


class InputManager(EngineComponent):

    def boot(self) -> bool:
        self.keyboard = Keyboard(self)
        self.mouse = Mouse(self)
        return True

    def ready(self) -> None:
        pass

    def teardown(self) -> None:
        pass

    def cycle(self) -> None:
        pass
