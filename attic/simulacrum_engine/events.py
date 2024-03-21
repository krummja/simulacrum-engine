from __future__ import annotations
from typing import *
if TYPE_CHECKING:
    pass


@runtime_checkable
class Listener(Protocol):

    def __call__(self, *args: Any, **kwargs: Any) -> Any:
        ...


class ListenerWrapper:

    def __init__(self, listener: Listener, is_once: bool = False) -> None:
        self.listener = listener
        self.is_once = is_once

    def __call__(self, *args: Any, **kwargs: Any) -> None:
        self.listener(*args, **kwargs)

    def __eq__(self, other: ListenerWrapper | Listener) -> bool:
        if isinstance(other, ListenerWrapper):
            return other.listener == self.listener
        if isinstance(other, Listener):
            return other == self.listener

    def __repr__(self) -> str:
        return str(self.listener)


class Emitter:

    def __init__(self) -> None:
        self.events: dict[str, list[ListenerWrapper]] = {}

    def on(self, event: str, listener: Listener) -> None:
        self._on(event, ListenerWrapper(listener))

    def once(self, event: str, listener: Listener) -> None:
        self._on(event, ListenerWrapper(listener, is_once=True))

    def emit(self, event: str, *args: Any, **kwargs: Any) -> None:
        if event in self.events:
            for listener in self.events[event][:]:
                if listener.is_once:
                    self.remove(event, listener)
                listener(*args, **kwargs)

    def remove(self, event: str, listener: Listener) -> None:
        if event in self.events:
            events = self.events[event]
            if listener in events:
                events.remove(listener)

    def count(self, event: str) -> int:
        return len(self.events[event]) if event in self.events else 0

    def _on(self, event: str, listener_wrapper: ListenerWrapper) -> None:
        if event not in self.events:
            self.events[event] = []
        self.events[event].append(listener_wrapper)


def on(emitter: Emitter, event: str):
    def decorator(listener: Listener):
        emitter.on(event, listener)
        return listener
    return decorator


def once(emitter: Emitter, event: str):
    def decorator(listener: Listener):
        emitter.once(event, listener)
        return listener
    return decorator
