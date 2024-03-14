from __future__ import annotations
from typing import *
if TYPE_CHECKING:
    pass

import pecs_framework as pecs

from simulacrum_engine.core.component import EngineComponent
from simulacrum_engine.core.events import Events


class ECSManager(EngineComponent):

    def boot(self) -> bool:
        return True

    def ready(self) -> None:
        self.emitter.emit(
            Events.LOG_INFO,
            message="ECSManager passed readiness check",
            symbol="success",
        )

    def teardown(self) -> None:
        pass

    def cycle(self) -> None:
        pass
