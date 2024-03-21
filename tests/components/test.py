from __future__ import annotations
from dataclasses import dataclass
import pecs_framework as pecs


@dataclass
class Test(pecs.Component):
    prop: str

    def on_update(self) -> None:
        print(f"{self.prop} Update!")
