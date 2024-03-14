from __future__ import annotations
from typing import *
if TYPE_CHECKING:
    pass

from simulacrum_engine.core.component import EngineComponent
from .window import Window


class WindowManager(EngineComponent):

    def boot(self) -> bool:
        self.window = Window()
        return True

    def ready(self) -> None:
        pass

    def teardown(self) -> None:
        pass

    def cycle(self) -> None:
        pass
