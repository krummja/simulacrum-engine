from __future__ import annotations
from typing import *
if TYPE_CHECKING:
    pass

import os
import json
from pathlib import Path


def read_json(path: str | Path) -> dict[str, Any]:
    file = open(path, "r")
    data = json.load(file)
    file.close()
    return data
