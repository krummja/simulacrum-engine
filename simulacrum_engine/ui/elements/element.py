from __future__ import annotations
from typing import *
if TYPE_CHECKING:
    from simulacrum_engine.ui.ui_manager import UIManager

from dataclasses import dataclass
import pygame as pyg

from simulacrum_engine.rendering.color import Color
from enum import StrEnum
from devtools import debug

from nutree import Node


class MouseEventType(StrEnum):
    CLICK = "CLICK"
    DBL_CLICK = "DBL_CLICK"
    MOUSEDOWN = "MOUSEDOWN"
    MOUSEUP = "MOUSEUP"
    ENTER = "ENTER"
    OVER = "OVER"
    MOVE = "MOVE"
    OUT = "OUT"
    LEAVE = "LEAVE"


@dataclass(slots=True, frozen=True)
class MouseEvent:
    event_type: MouseEventType
    x: float
    y: float


class MouseCallback(Protocol):
    def __call__(self, event: MouseEvent) -> None:
        ...


def MOUSE_NOOP(event: MouseEvent) -> None:
    return


class ElementProps(TypedDict):
    x: NotRequired[float]
    y: NotRequired[float]
    height: NotRequired[float]
    width: NotRequired[float]
    foreground: NotRequired[Color]
    background: NotRequired[Color]
    on_mouse_enter: NotRequired[MouseCallback]
    on_mouse_leave: NotRequired[MouseCallback]


DEFAULT_PROPS: ElementProps = {
    "x": 0,
    "y": 0,
    "height": 0,
    "width": 0,
    "foreground": Color(255, 255, 255),
    "background": Color(0, 0, 0),
    "on_mouse_enter": MOUSE_NOOP,
    "on_mouse_leave": MOUSE_NOOP,
}


class Element:

    def __init__(self, ui_manager: UIManager, id: str) -> None:
        self.ui_manager = ui_manager
        self.id = id
        self._tree = ui_manager.tree
        self._is_mouse_over = False
        self._is_visible = False

    @property
    def is_visible(self) -> bool:
        return self._is_visible

    def initialize(self, props: ElementProps | None = None) -> Self:
        if props is None:
            props = DEFAULT_PROPS
        else:
            for k, v in DEFAULT_PROPS.items():
                if k not in props:
                    props[k] = v

        self.x = props["x"]
        self.y = props["y"]
        self.height = props["height"]
        self.width = props["width"]
        self.foreground = props["foreground"]
        self.background = props["background"]
        self.on_mouse_enter = props["on_mouse_enter"]
        self.on_mouse_leave = props["on_mouse_leave"]

        self.rect = pyg.Rect(self.x, self.y, self.width, self.height)
        self.surface = pyg.Surface((self.width, self.height))

        self.setup()
        return self

    def check_mouse_enter(self) -> None:
        m_pos = self.ui_manager.input.mouse.position
        cursor = self.ui_manager.input.mouse.cursor
        if not self._is_mouse_over and self.rect.contains(cursor):
            self._is_mouse_over = True
            self.on_mouse_enter(MouseEvent(MouseEventType.ENTER, *m_pos))

    def check_mouse_leave(self) -> None:
        m_pos = self.ui_manager.input.mouse.position
        cursor = self.ui_manager.input.mouse.cursor
        if self._is_mouse_over and not self.rect.contains(cursor):
            self._is_mouse_over = False
            self.on_mouse_leave(MouseEvent(MouseEventType.LEAVE, *m_pos))

    def setup(self) -> None:
        ...

    def cycle(self) -> None:
        self.check_mouse_enter()
        self.check_mouse_leave()

        self.surface.fill(self.background)
        self.ui_manager.renderer.blit({
            "source": self.surface,
            "position": (self.x, self.y),
        }, z_level=110, group="default")
