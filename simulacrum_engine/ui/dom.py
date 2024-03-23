from __future__ import annotations
from typing import *
if TYPE_CHECKING:
    pass

import treeswift


class DOM:

    def __init__(self) -> None:
        self.root = treeswift.Tree()


