from __future__ import annotations
from typing import *
if TYPE_CHECKING:
    pass

import pecs_framework as pecs
from pecs_framework import BaseSystem

from ..components import Sprite


class RenderSystem(BaseSystem):

    def initialize(self):
        self.query("renderables", all_of=[Sprite])

    def update(self) -> None:
        renderables = self._queries["renderables"].result
        for renderable in renderables:
            pass
