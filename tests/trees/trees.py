from __future__ import annotations
from typing import *
if TYPE_CHECKING:
    pass

from rich import inspect
from dataclasses import dataclass, KW_ONLY
from nutree import Tree, Node


@dataclass(unsafe_hash=True)
class Element:
    id: str
    x: int = 0
    y: int = 0
    w: int = 0
    h: int = 0

    def compute_dims(self) -> None:
        print("computing")


tree = Tree("ui")
a = tree.add_child(Element(id="A", x=10, y=10, w=100, h=100))
b = tree.add_child(Element(id="B", x=10, y=10, w=100, h=100))
c = b.add_child(Element(id="C", x=10, y=10, w=100, h=100))


res = tree.find_all(match=lambda n: n.data.id == "A")
print(res)

res = tree.find_all(match=lambda n: n.data.id == "C")
print([n.parent for n in res])
