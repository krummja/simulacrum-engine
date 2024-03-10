from __future__ import annotations
from typing import *
if TYPE_CHECKING:
    from moderngl import Buffer

import moderngl
from moderngl import Texture
from pathlib import Path

from array import array
from textwrap import dedent
from pygame import Surface

from simulacrum_engine.render_object import RenderObject


def default_vert_shader() -> str:
    return dedent("""//glsl
        #version 330

        in vec2 vert;
        in vec2 texcoord;
        out vec2 uv;

        void main() {
            uv = texcoord;
            gl_Position = vec4(vert, 0.0, 1.0);
        }
    """)

def default_frag_shader() -> str:
    return dedent("""//glsl
        # version 330

        uniform sampler2D surface;

        out vec4 f_color;
        in vec2 uv;

        void main() {
            f_color = vec4(texture(surface, uv).rgb, 1.0);
        }
    """)


class MGL:

    def __init__(self) -> None:
        self.ctx = moderngl.create_context(require=330)

        self.quad_buffer = self.ctx.buffer(data=array('f', [
            -1.0,  1.0,  0.0,  0.0,
            -1.0, -1.0,  0.0,  1.0,
             1.0,  1.0,  1.0,  0.0,
             1.0, -1.0,  1.0,  1.0
        ]))

        self.quad_buffer_notex = self.ctx.buffer(data=array('f', [
            -1.0,  1.0,
            -1.0, -1.0,
             1.0,  1.0,
             1.0, -1.0
        ]))

        self.default_vert = default_vert_shader()
        self.default_frag = default_frag_shader()

    def default_render_object(self) -> RenderObject:
        return RenderObject(self, self.default_frag, use_default=True)

    def render_object(
        self,
        frag_path: Path,
        vert_shader: str | None = None,
        vao_args: list[str] | None = None,
        buffer: Buffer | None = None
    ) -> RenderObject:
        if vao_args is None:
            vao_args = ["2f 2f", "vert", "texcoord"]
        frag_shader = read_f(frag_path)
        if vert_shader is not None:
            vert_shader = read_f(Path(vert_shader))

        return RenderObject(
            self,
            frag_shader,
            vert_shader,
            vao_args=vao_args,
            buffer=buffer,
        )

    def pg_to_tex(self, surface: Surface) -> Texture:
        channels = 4
        texture = self.ctx.texture(surface.get_size(), channels)
        texture.filter = (moderngl.NEAREST, moderngl.NEAREST)
        texture.swizzle = "BGRA"
        texture.write(surface.get_view("1"))
        return texture

    def pg_to_tex_update(self, texture: Texture, surface: Surface) -> Texture:
        texture.write(surface.get_view("1"))
        return texture


def read_f(path: Path) -> str:
    file = open(path, "r")
    data = file.read()
    file.close()
    return data
