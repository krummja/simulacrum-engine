from __future__ import annotations
from typing import *
if TYPE_CHECKING:
    pass

from simulacrum_engine.core.logger import log_boot
from simulacrum_engine.core.component import EngineComponent


class SoundManager(EngineComponent):

    @log_boot
    def boot(self) -> bool:
        return True

    def ready(self) -> None:
        pass

    def teardown(self) -> None:
        pass

    def cycle(self) -> None:
        pass
