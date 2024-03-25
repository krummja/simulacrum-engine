from __future__ import annotations
from typing import *
if TYPE_CHECKING:
    pass

import pygame as pyg
from simulacrum_engine.component import EngineComponent
from simulacrum_engine.rendering.render_manager import RenderManager
from simulacrum_engine.events import Events

from .window import Window


class WindowManager(EngineComponent):

    def boot(self) -> bool:
        self.window = Window(
            self.engine.config.window,
            self.engine.config.shader,
        )

        failures = self.window.pygame_init_failures
        self.emitter.emit(
            Events.LOG_INFO,
            message=f"Detected {failures} PyGame init failures",
            symbol="success" if failures == 0 else "error",
        )

        sdl_version = pyg.get_sdl_version()
        sdl_version_str = ".".join([str(part) for part in sdl_version])
        self.emitter.emit(
            Events.LOG_INFO,
            message=f"Using SDL Version {sdl_version_str}",
            symbol="info",
        )

        self.emitter.on(Events.POST_UPDATE, self.cycle)
        self.uniforms = self.engine[RenderManager].uniforms
        return True

    def cycle(self) -> None:
        self.window.cycle({
            "surface": self.uniforms["default"],
            "ui_surf": self.uniforms["ui_surf"],
        })

    @property
    def delta(self) -> float:
        return self.window.frame_manager.frame_delta

    @property
    def fps(self) -> float:
        return self.window.frame_manager.fps
