from simulacrum_engine.core import *
from rich import inspect

from pathlib import Path


class RenderManagerBoot:

    def __call__(self) -> bool:
        return True


class Game:

    def __init__(self) -> None:
        self.engine = Engine()

    def start(self) -> None:
        self.engine.boot()
        inspect(self.engine)


if __name__ == '__main__':
    game = Game()
    game.start()
