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

        # If `opengl` is enabled in the project config, tell PyGame to use OpenGL
        # rendering with double buffering.
        # When the `DOUBLEBUF` flag is set, the display waits for vertical retrace.
        # By default, this results in surfaces being swapped. When `OPENGL` is also
        # set, PyGame will perform a GL buffer swap instead.
        if self.opengl:
            self.flags = self.flags | pyg.DOUBLEBUF | pyg.OPENGL

        self.background_color = (21, 21, 21)

        self.frame_manager = FrameManager(self)
        self.screen = Screen(self)
        self.pygame_init_failures = self.screen.pygame_init_failures

        if window.icon_path:
            icon = pyg.image.load(window.icon_path).convert_alpha()
            pyg.display.set_icon(icon)

    def cycle(self, uniforms: dict[str, Any] | None = None) -> None:
        self.screen.cycle(uniforms)
        self.frame_manager.cycle()

        self.screen.clear()
        self.frame_manager.next_frame()
