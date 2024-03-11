from __future__ import annotations
from typing import *
if TYPE_CHECKING:
    pass

import sys
import pygame as pyg
from pathlib import Path

from simulacrum_engine.window import Window
from simulacrum_engine.input import Input
from simulacrum_engine.renderer import Renderer
from simulacrum_engine.config import Config


class Game:

    def __init__(self, config_path: Path | str, config_file: str) -> None:
        self.config = Config(config_path, config_file)
        self.window_config = self.config.window
        self.shader_config = self.config.shader
        self.input_config = self.config.input

        # Window & Graphics Setup
        self.window = Window(self.window_config, self.shader_config)
        self.display_size = (
            self.window_config.width // self.window_config.render_scale,
            self.window_config.height // self.window_config.render_scale,
        )

        # Input Setup
        self.input = Input(self.input_config)
        self.window.bind_input(self.input)

        # Renderer Setup
        self.renderer = Renderer()
        self.renderer.set_groups(["ui", "default"])

        self.display = pyg.Surface(self.display_size)
        self.ui_surf = pyg.Surface(self.display_size, pyg.SRCALPHA)

    def load(self) -> None:
        raise NotImplementedError("Game must implement `load` method.")

    def update(self) -> None:
        raise NotImplementedError("Game must implement `update` method.")

    def run(self) -> None:
        self.load()
        while True:
            self.update()

    def quit(self) -> None:
        pyg.quit()
        sys.exit()
