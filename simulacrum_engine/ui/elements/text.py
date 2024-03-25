from __future__ import annotations
from typing import *
if TYPE_CHECKING:
    from simulacrum_engine.rendering.renderer import Renderer

from pathlib import Path
import pygame as pyg

from simulacrum_engine import io_tools
from simulacrum_engine.rendering import gfx_tools
from simulacrum_engine.rendering.color import Color

from devtools import debug


FontImageData = tuple[list[pyg.Surface], list[int], int]


def load_font_image(path: Path, color: Color = Color(255, 255, 255)) -> FontImageData:
    fg_color = Color(255, 0, 0)
    bg_color = Color(0, 0, 0)

    font_img = pyg.image.load(path).convert_alpha()
    font_img = gfx_tools.palette_swap(font_img, {fg_color : color})

    last_x = 0
    letters: list[pyg.Surface] = []
    letter_spacing: list[int] = []

    for x in range(font_img.get_width()):
        if font_img.get_at((x, 0))[0] == 127:
            letters.append(
                gfx_tools.clip(
                    font_img,
                    pyg.Rect(last_x, 0, x - last_x, font_img.get_height()),
                )
            )

            letter_spacing.append(x - last_x)
            last_x = x + 1
        x += 1

    for letter in letters:
        letter.set_colorkey(bg_color)

    return letters, letter_spacing, font_img.get_height()


class UIText:

    def __init__(self, path: Path | None = None) -> None:
        self.path = path
        self.fonts: dict[str, Font] = {}
        self.load()

    def load(self, path: Path | None = None) -> None:
        if path:
            self.path = path
        if self.path:
            self.fonts = io_tools.recursive_file_op(
                self.path,
                Font,
                filetype="png",
            )

    def __getitem__(self, key: str) -> Font:
        return self.fonts[key]


class PreppedText:

    def __init__(self, text: str, size: tuple[int, int], font: Font) -> None:
        self.text = text
        self.size = size
        self.width = size[0]
        self.height = size[1]
        self.font = font


class RenderFontParams(TypedDict):
    text: str
    loc: tuple[int, int]
    line_width: NotRequired[int]
    color: NotRequired[Color]


FONT_ORDER = [
    'A','B','C','D','E','F','G','H','I','J','K','L','M',
    'N','O','P','Q','R','S','T','U','V','W','X','Y','Z',
    'a','b','c','d','e','f','g','h','i','j','k','l','m',
    'n','o','p','q','r','s','t','u','v','w','x','y','z',
    '.','-',',',':','+','\'','!','?',
    '0','1','2','3','4','5','6','7','8','9',
    '(',')','/','_','=','\\','[',']','*','"','<','>',';',
]


class Font:

    def __init__(self, path: Path, color: Color = Color(255, 255, 255)) -> None:
        self.base_color = color
        self.letters, self.spacing, self.line_height = load_font_image(path, color)

        self.color_cache = {color: self.letters}
        self.font_map = {k: i for i, k in enumerate(FONT_ORDER)}
        self.space_width = self.spacing[0]
        self.base_spacing = 1
        self.line_spacing = 2

    def prep_color(self, color: Color) -> None:
        new_letters = []
        for img in self.letters:
            if len(color) > 3:
                img.convert_alpha()

            surf = gfx_tools.palette_swap(img, {self.base_color:color})
            new_letters.append(surf)

        self.color_cache[color] = new_letters

    def render_with(
        self,
        renderer: Renderer,
        params: RenderFontParams,
        z_level: int = 0,
        group: str = "default",
    ) -> None:
        if "color" not in params:
            color = self.base_color
        if color not in self.color_cache:
            self.prep_color(color)
        letters = self.color_cache[color]
        x_offset = 0
        y_offset = 0

        text = params["text"]

        if "line_width" in params and params['line_width'] is not None:
            line_width = params["line_width"]
            spaces = []
            x = 0
            for i, char in enumerate(text):
                if char == "\n":
                    continue
                if char == " ":
                    spaces.append((x, i))
                    x += self.space_width + self.base_spacing
                else:
                    x += self.spacing[self.font_map[char]] + self.base_spacing

            line_offset = 0

            for i, space in enumerate(spaces):
                if (space[0] - line_offset) > line_width:
                    line_offset += spaces[i - 1][0] - line_offset
                    if i != 0:
                        pre_space = text[:spaces[i - 1][1]]
                        post_space = text[spaces[i - 1][1] + 1:]
                        params['text'] = (pre_space + "\n" + post_space)

        loc = params['loc']

        for char in text:
            if char not in ["\n", " "]:
                renderer.blit({
                    'source': letters[self.font_map[char]],
                    "position": (loc[0] + x_offset, loc[1] + y_offset),
                }, z_level=z_level, group=group)

                x_offset += self.spacing[self.font_map[char]] + self.base_spacing
            elif char == " ":
                x_offset += self.space_width + self.base_spacing
            else:
                y_offset += self.line_spacing + self.line_height
                x_offset = 0
