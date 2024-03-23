from __future__ import annotations
from typing import *
if TYPE_CHECKING:
    from simulacrum_engine.config import InputConfig

import pygame as pyg
from .input_method import InputMethod


class Mouse(InputMethod):

    def setup(self, config: InputConfig) -> None:
        self.position = pyg.Vector2(0, 0)
        self.ui_position = pyg.Vector2(0, 0)
        self.movement = pyg.Vector2(0, 0)

    def update(self) -> None:
        m_pos = pyg.mouse.get_pos()
        self.movement = pyg.Vector2(
            m_pos[0] - self.position[0],
            m_pos[1] - self.position[1],
        )

        self.position = pyg.Vector2(m_pos[0], m_pos[1])
        self.ui_position = pyg.Vector2(m_pos[0] // 2, m_pos[1] // 2)
