from __future__ import annotations
from typing import *
if TYPE_CHECKING:
    from simulacrum_engine.input.input_manager import InputManager
    from simulacrum_engine.ui import Element, ElementProps

from pathlib import Path
import pygame as pyg
import pecs_framework as pecs

from simulacrum_engine.rendering.render_manager import RenderManager
from simulacrum_engine.window import WindowManager
from simulacrum_engine.ecs import ECSManager
from simulacrum_engine.component import EngineComponent
from simulacrum_engine.events import Events
from simulacrum_engine.input import InputManager
from simulacrum_engine.ui.elements.text import UIText


class UIManager(EngineComponent):

    def boot(self) -> bool:
        self.config = self.engine.config.asset
        self.renderer = self.engine[RenderManager].renderer
        self.text = UIText(Path(self.config.asset_path, "fonts"))
        self.emitter.on(Events.UPDATE, self.cycle)
        self.elements: OrderedDict[str, Element] = OrderedDict()
        return True

    @property
    def input(self) -> InputManager:
        return self.engine[InputManager]

    def add_element(self, id: str, element: type[Element], props: ElementProps) -> None:
        instance = element(self, id)
        self.elements[instance.id] = instance.initialize(props)

    def cycle(self) -> None:
        if self.engine.config.window.debug:
            fps = self.engine[WindowManager].fps
            ticks = self.engine[ECSManager].loop.ticks

            for element in self.elements.values():
                element.cycle()

            # self.text["large_font"].render_with(self.renderer, {
            #     "text": f"FPS: {round(fps)}",
            #     "loc": (8, 8 * 1),
            # })

            # self.text["large_font"].render_with(self.renderer, {
            #     "text": f"TCK: {round(ticks)}",
            #     "loc": (8, 8 * 4),
            # })
