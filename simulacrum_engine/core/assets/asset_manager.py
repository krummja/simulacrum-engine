from __future__ import annotations
from typing import *
if TYPE_CHECKING:
    pass

import time

from simulacrum_engine.core.component import EngineComponent
from simulacrum_engine.core.events import Events

from .asset_utils import recursive_file_op


class AssetManager(EngineComponent):

    def boot(self) -> bool:
        self.emitter.emit(
            Events.LOG_INFO,
            message="AssetManager booting...",
        )

        time.sleep(3)

        self.emitter.emit(
            Events.LOG_INFO,
            message="AssetManager boot complete.",
            symbol="success",
        )
        return True

    def ready(self) -> None:
        pass

    def teardown(self) -> None:
        pass

    def cycle(self) -> None:
        pass
