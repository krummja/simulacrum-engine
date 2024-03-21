from __future__ import annotations
from types import ModuleType

import pecs_framework as pecs

from tests import components


class Loader(pecs.Loader):

    def __init__(self, root_module: ModuleType) -> None:
        self._root = root_module
        self._components = []

    def load(self) -> None:
        component_map = map(components.__dict__.get, components.__all__)
        for component in component_map:
            self._components.append(component)
