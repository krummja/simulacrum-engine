from __future__ import annotations
from typing import *
if TYPE_CHECKING:
    from simulacrum_engine.core.engine import Engine

from simulacrum_engine._types import Bases, Namespace


class ComponentMeta(type):

    id: str

    def __new__(cls, name: str, bases: Bases, namespace: Namespace) -> ComponentMeta:
        clsobj = super().__new__(cls, name, bases, namespace)
        clsobj.id = name
        return clsobj


class EngineComponent(metaclass=ComponentMeta):

    def __init__(self, engine: Engine) -> None:
        self.engine = engine
        self.emitter = self.engine.emitter
        self.logger = self.engine.logger

    def boot(self) -> bool:
        raise NotImplementedError("Method has not been implemented.")

    def ready(self) -> None:
        raise NotImplementedError("Method has not been implemented.")

    def teardown(self) -> None:
        raise NotImplementedError("Method has not been implemented.")

    def cycle(self) -> None:
        raise NotImplementedError("Method has not been implemented.")
