from __future__ import annotations
from typing import *
if TYPE_CHECKING:
    pass

import sys
import pygame as pyg
from pathlib import Path

import pecs_framework as pecs

from simulacrum_engine.window import Window
from simulacrum_engine.input import Input
from simulacrum_engine.renderer import Renderer
from simulacrum_engine.config import Config


class Loop(pecs.base_system.Loop):

    def __init__(self, game: Game, ecs: pecs.Engine, domain: pecs.Domain) -> None:
        self.game = game
        super().__init__(ecs, domain)

    def initialize(self) -> None:
        raise NotImplementedError("Method has no implementation")

    def teardown(self) -> None:
        raise NotImplementedError("Method has no implementation")

    def pre_update(self) -> None:
        raise NotImplementedError("Method has no implementation")

    def update(self) -> None:
        raise NotImplementedError("Method has no implementation")

    def post_update(self) -> None:
        raise NotImplementedError("Method has no implementation")


class Game:

    def __init__(
        self,
        config_path: Path | str,
        config_file: str,
        loader: pecs.Loader | None = None,
        loop: type[pecs.base_system.Loop] | None = None,
    ) -> None:
        self.config = Config(config_path, config_file)
        self.window_config = self.config.window
        self.shader_config = self.config.shader
        self.input_config = self.config.input
        self.ecs_config = self.config.ecs

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

        # ECS Setup, if enabled
        if self.ecs_config.enable:
            self.ecs = pecs.Engine(loader)
            self.domain = self.ecs.create_domain(self.ecs_config.domain_id)

            if loop is None:
                raise Exception("ecs.enabled requires a Loop instance passed to Game.")
            self.loop = loop(self.ecs, self.domain)

        # Main display surfaces
        self.display = pyg.Surface(self.display_size)
        self.ui_surf = pyg.Surface(self.display_size, pyg.SRCALPHA)

    def load(self) -> None:
        raise NotImplementedError("Game must implement `load` method.")

    def update(self) -> None:
        raise NotImplementedError("Game must implement `update` method.")

    def run(self) -> None:
        self.load()
        if self.ecs_config.enable:
            self.loop.initialize()

        while True:
            if self.ecs_config.enable:
                self.loop.pre_update()
                self.loop.update()

            self.update()

            if self.ecs_config.enable:
                self.loop.post_update()

    def quit(self) -> None:
        if self.ecs_config.enable:
            self.loop.teardown()
        pyg.quit()
        sys.exit()
