from __future__ import annotations
from typing import *
if TYPE_CHECKING:
    pass

import time

from simulacrum_engine.core.component import EngineComponent
from simulacrum_engine.core.events import Events
from simulacrum_engine.core.logger import log_boot

from .asset_utils import recursive_file_op


class AssetManager(EngineComponent):

    def boot(self) -> bool:
        return True

    def ready(self) -> None:
        pass

    def teardown(self) -> None:
        pass

    def cycle(self) -> None:
        pass
