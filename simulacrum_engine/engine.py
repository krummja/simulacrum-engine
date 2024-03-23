from __future__ import annotations
from typing import *

if TYPE_CHECKING:
    from simulacrum_engine.component import EngineComponent

import sys
import pygame as pyg
from devtools import debug

from simulacrum_engine.assets import AssetManager
from simulacrum_engine.config import Config
from simulacrum_engine.ecs import ECSManager
from simulacrum_engine.events import Emitter
from simulacrum_engine.events import Events
from simulacrum_engine.input import InputManager
from simulacrum_engine.logger import Logger
from simulacrum_engine.physics import PhysicsManager
from simulacrum_engine.rendering import RenderManager
from simulacrum_engine.sound import SoundManager
from simulacrum_engine.window import WindowManager
from simulacrum_engine.ui.ui_manager import UIManager

from simulacrum_engine.component import EC


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
        ui_manager: type[UIManager] = UIManager,
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

        ui_params = init_mapping.get(UIManager.id, {})
        self.initialize_component(ui_manager, **ui_params)

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
            self.shutdown()

    def boot(self) -> None:
        if all([component.is_booted for component in self.components.values()]):
            self.emitter.emit(Events.LOG_INFO, message="Engine boot", symbol="success")
            self._is_booted = True
            self.ready()
        else:
            self.emitter.emit(Events.LOG_INFO, message="Engine boot", symbol="error")

    def ready(self) -> None:
        self.emitter.emit(Events.LOG_INFO, message="Engine ready", symbol="success")
        self.emitter.emit(Events.READY)
        self.run()

    def teardown(self) -> None:
        self.emitter.emit(Events.LOG_INFO, message="Shutting down...")
        self.emitter.emit(Events.TEARDOWN)
        # TODO: Give engine components time to teardown and return a response
        self.shutdown()

    def shutdown(self) -> None:
        self.emitter.emit(Events.LOG_INFO, message="Shutdown complete. Goodbye!")
        pyg.quit()
        sys.exit()

    def run(self) -> None:
        while True:
            self.cycle()

    def cycle(self) -> None:
        self.emitter.emit(Events.PRE_UPDATE)
        self.emitter.emit(Events.UPDATE)
        self.emitter.emit(Events.POST_UPDATE)
