from __future__ import annotations
from typing import *
if TYPE_CHECKING:
    from simulacrum_engine.ecs.loop import Loop
    from simulacrum_engine.engine import Engine

import pecs_framework as pecs


class System(pecs.BaseSystem):

    def __init__(self, engine: Engine, loop: Loop) -> None:
        self.engine = engine
        super().__init__(loop)
