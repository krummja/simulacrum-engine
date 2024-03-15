from __future__ import annotations
from typing import *
if TYPE_CHECKING:
    pass

from pathlib import Path


def read_file_to_str(path: Path | str) -> str:
    if not isinstance(path, Path):
        path = Path(path)
    file = open(path, "r")
    data = file.read()
    file.close()
    return data
