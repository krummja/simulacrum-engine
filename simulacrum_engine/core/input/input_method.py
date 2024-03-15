from __future__ import annotations
from typing import *
if TYPE_CHECKING:
    from .input_manager import InputManager
    from simulacrum_engine.core.config import InputConfig


class InputMethod:

    def __init__(self, input_manager: InputManager) -> None:
        self.input_manager = input_manager
        self.setup(self.input_manager.config)

    def setup(self, config: InputConfig) -> None:
        raise NotImplementedError("Method has no implementation.")
