from __future__ import annotations
from typing import *

if TYPE_CHECKING:
    pass

import pygame as pyg

from simulacrum_engine.config import WindowConfig
from simulacrum_engine.config import ShaderConfig

from .screen import Screen
from .frame_manager import FrameManager


class Window:
    """
    Window object wrapping the FrameManager and Screen.

    In opengl mode, the Screen passes its internal PyGame display as the RenderObject
    surface.
    """

    def __init__(
        self,
        window: WindowConfig,
        shader: ShaderConfig,
    ) -> None:
        self.dimensions = (window.width, window.height)
        self.title = window.title
        self.icon_path = window.icon_path
        self.flags = pyg.RESIZABLE if window.resizable else 0
        self.fps_cap = window.fps_cap

        self.opengl = shader.opengl
        self.fragment_path = shader.fragment_path

        if self.opengl:
            self.flags = self.flags | pyg.DOUBLEBUF | pyg.OPENGL

        self.background_color = (21, 21, 21)

        self.frame_manager = FrameManager(self)
        self.screen = Screen(self)

        if window.icon_path:
            icon = pyg.image.load(window.icon_path).convert_alpha()
            pyg.display.set_icon(icon)

    def cycle(self, uniforms: dict[str, Any] | None = None) -> None:
        self.screen.cycle(uniforms)
        self.frame_manager.cycle()

        self.screen.clear()
        self.frame_manager.next_frame()
