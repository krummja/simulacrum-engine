from __future__ import annotations
from typing import *
if TYPE_CHECKING:
    pass

import time

from simulacrum_engine.component import EngineComponent
from simulacrum_engine.events import Events

from .asset import Asset
from .asset import AssetType


AssetMap: TypeAlias = dict[AssetType, dict[str, list[Asset]]]


class AssetManager(EngineComponent):

    def boot(self) -> bool:
        self.assets: AssetMap = {}
        return True

    def ready(self) -> None:
        pass

    def teardown(self) -> None:
        pass

    def cycle(self) -> None:
        pass
