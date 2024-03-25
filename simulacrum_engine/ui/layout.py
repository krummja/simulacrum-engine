from __future__ import annotations
from typing import *
if TYPE_CHECKING:
    pass

from dataclasses import dataclass, KW_ONLY
from nutree import Tree
from nutree import Node
from nutree import SkipBranch
from nutree import StopTraversal
from nutree import SelectBranch
from nutree import AmbiguousMatchError

from enum import StrEnum


class Direction(StrEnum):
    LEFT_TO_RIGHT = "LEFT_TO_RIGHT"
    RIGHT_TO_LEFT = "RIGHT_TO_LEFT"
    TOP_DOWN = "TOP_DOWN"
    BOTTOM_UP = "BOTTOM_UP"


class Align(StrEnum):
    MIN = "MIN"
    CENTER = "CENTER"
    MAX = "MAX"


class Layout:

    def __init__(self) -> None:
        self.tree = Tree()

    def add_node(self) -> None:
        pass


@dataclass(kw_only=True, unsafe_hash=True)
class Element:
    id: str
    x: float = 0.0
    y: float = 0.0
    height: float = 0.0
    width: float = 0.0
    padding_top: float = 0.0
    padding_right: float = 0.0
    padding_bottom: float = 0.0
    padding_left: float = 0.0


def layout(node: Node, memo: list) -> None:
    if len(memo) > 0:
        previous = memo[-1]

        if node.data.x <= previous.x + previous.padding_left:
            node.data.x = previous.x + previous.padding_left
            node.data.x += node.data.padding_left

        if node.data.y <= previous.y:
            node.data.y = previous.y + previous.padding_top
            node.data.y += node.data.padding_top

    if node.has_children:
        memo.append(node.data)
    print(memo)


if __name__ == '__main__':
    root = Tree(name="layout")

    test = root.add_child(
        Element(
            id="Test",
            x=10.0,
            y=30.0,
            padding_left=10,
            padding_top=15,
        ),
    )

    test.append_child(Element(id="Test-2"))

    root.visit(layout, memo=[])
    root.print()
