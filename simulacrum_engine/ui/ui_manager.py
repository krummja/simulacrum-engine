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

from nutree import Tree, Node


class UIManager(EngineComponent):

    def boot(self) -> bool:
        self.config = self.engine.config.asset
        self.renderer = self.engine[RenderManager].renderer
        self.tree = Tree("ui")

        self.emitter.on(Events.UPDATE, self.cycle)
        return True

    @property
    def input(self) -> InputManager:
        return self.engine[InputManager]

    def add_element(self, id: str, element: type[Element], props: ElementProps) -> None:
        elem = self.tree.add_child(element(self, id))
        elem.data.initialize(props)

    def add_child_for_element(
        self,
        parent_id: str,
        child_id: str,
        element: type[Element],
        props: ElementProps,
    ) -> None:
        if node := self.find_element(parent_id):
            child = node.add_child(element(self, child_id))
            child.data.initialize(props)

    def find_element(self, id: str) -> Node | None:
        result = self.tree.find(match=lambda n: n.data.id == id)
        if result is not None:
            return result

    def get_parent_for_element(self, id: str) -> Node | None:
        if element := self.find_element(id):
            return element.parent

    def get_childen_for_element(self, id: str) -> list[Node] | None:
        if element := self.find_element(id):
            return element.children

    def cycle(self) -> None:
        if self.engine.config.window.debug:
            fps = self.engine[WindowManager].fps
            ticks = self.engine[ECSManager].loop.ticks

            for element in self.tree.iterator():
                element.data.cycle()
