from simulacrum_engine.core import *
from rich import inspect

from pathlib import Path


def test_setup() -> None:
    engine = Engine(config=Config())
    engine.boot()


if __name__ == '__main__':
    test_setup()
