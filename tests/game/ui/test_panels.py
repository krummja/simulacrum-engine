from __future__ import annotations
from typing import *
if TYPE_CHECKING:
    pass

from simulacrum_engine import *
from simulacrum_engine.ui.elements.panel import Panel


def setup_test_panels(ui_manager: UIManager) -> None:
    ui_manager.add_element("panel_01", Panel, {
        "x": 10,
        "y": 10,
        "width": 200,
        "height": 400,
        "background": Color(55, 55, 55),
        "on_mouse_enter": (lambda event: print(event)),
        "on_mouse_leave": (lambda event: print(event)),
    })

    ui_manager.add_child_for_element(
        parent_id="panel_01",
        child_id="panel_01_a",
        element=Panel,
        props={
            "x": 20,
            "y": 20,
            "width": 180,
            "height": 380,
            "background": Color(85, 85, 85),
        },
    )
