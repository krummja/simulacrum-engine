from __future__ import annotations
from typing import *
if TYPE_CHECKING:
    from .input_manager import InputManager


class InputMethod:

    def __init__(self, input_manager: InputManager) -> None:
        self.input_manager = input_manager
