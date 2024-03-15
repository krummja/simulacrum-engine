from __future__ import annotations
from typing import *
if TYPE_CHECKING:
    from simulacrum_engine.core.config import InputConfig

from .input_method import InputMethod


class Mouse(InputMethod):

    def setup(self, config: InputConfig) -> None:
        pass
