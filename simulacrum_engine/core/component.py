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

    def __init__(self, engine: Engine, **kwargs: Any) -> None:
        self.engine = engine
        self.emitter = self.engine.emitter
        self.logger = self.engine.logger
        self._is_booted = self.boot(**kwargs)

    @property
    def is_booted(self) -> bool:
        return self._is_booted

    def boot(self, **kwargs: Any) -> bool:
        """
        Lifecycle method invoked for each component on engine boot.

        Implementation must return `True` by default and `False` only when some
        specified boot validation has failed (e.g. a needed resource could not be
        found).
        """
        raise NotImplementedError("Method has not been implemented.")

    def ready(self) -> None:
        raise NotImplementedError("Method has not been implemented.")

    def teardown(self) -> None:
        raise NotImplementedError("Method has not been implemented.")

    def cycle(self) -> None:
        raise NotImplementedError("Method has not been implemented.")


EC = TypeVar("EC", bound=EngineComponent)
