from __future__ import annotations
from typing import *

if TYPE_CHECKING:
    from simulacrum_engine.core.component import EngineComponent

import sys
import pygame as pyg
from devtools import debug

from simulacrum_engine.core.assets import AssetManager
from simulacrum_engine.core.config import Config
from simulacrum_engine.core.ecs import ECSManager
from simulacrum_engine.core.events import Emitter
from simulacrum_engine.core.events import Events
from simulacrum_engine.core.input import InputManager
from simulacrum_engine.core.logger import Logger
from simulacrum_engine.core.physics import PhysicsManager
from simulacrum_engine.core.rendering import RenderManager
from simulacrum_engine.core.sound import SoundManager
from simulacrum_engine.core.window import WindowManager

from simulacrum_engine.core.component import EC


class Engine:

    def __init__(
        self,
        *,
        config: Config = Config(),
        asset_manager: type[AssetManager] = AssetManager,
        ecs_manager: type[ECSManager] = ECSManager,
        input_manager: type[InputManager] = InputManager,
        physics_manager: type[PhysicsManager] = PhysicsManager,
        sound_manager: type[SoundManager] = SoundManager,
        window_manager: type[WindowManager] = WindowManager,
        render_manager: type[RenderManager] = RenderManager,
        init_mapping: dict[str, dict[str, Any]] | None = None
    ) -> None:
        self.config = config
        self.emitter = Emitter()
        self.logger = Logger(self)
        self.components: dict[str, EngineComponent] = {}

        init_mapping = init_mapping if init_mapping else {}

        self._is_booted = False

        self.initialize_component(render_manager)
        self.initialize_component(window_manager)
        self.initialize_component(input_manager)
        self.initialize_component(asset_manager)
        self.initialize_component(physics_manager)
        self.initialize_component(sound_manager)

        ecs_params = init_mapping.get(ECSManager.id, {})
        self.initialize_component(ecs_manager, **ecs_params)

    def __getitem__(self, key: type[EC] | str) -> EC:
        if isinstance(key, str):
            _component = self.components[key]
        else:
            _component = self.components[key.id]
        return cast(EC, _component)

    def initialize_component(
        self,
        component: type[EngineComponent],
        **init_kwargs: Any,
    ) -> None:
        initialized = component(self, **init_kwargs)
        self.emitter.on(Events.READY, initialized.ready)
        self.emitter.on(Events.TEARDOWN, initialized.teardown)
        self.components[initialized.id] = initialized

    def add_component(self, component: type[EngineComponent]) -> None:
        if not self._is_booted:
            self.initialize_component(component)
        else:
            self.quit()

    def boot(self) -> None:
        if all([component.is_booted for component in self.components.values()]):
            self._is_booted = True
            self.ready()

    def ready(self) -> None:
        self.emitter.emit(Events.READY)
        self.run()

    def teardown(self) -> None:
        self.emitter.emit(Events.TEARDOWN)
        self.quit()

    def quit(self) -> None:
        pyg.quit()
        sys.exit()

    def run(self) -> None:
        while True:
            self.cycle()

    def cycle(self) -> None:
        self.emitter.emit(Events.PRE_UPDATE)
        self.emitter.emit(Events.UPDATE)
        self.emitter.emit(Events.POST_UPDATE)
