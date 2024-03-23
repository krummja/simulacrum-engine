from __future__ import annotations
from typing import *
if TYPE_CHECKING:
    from moderngl import Buffer

from pathlib import Path
from array import array
from textwrap import dedent

import moderngl as mgl
import pygame as pyg

from simulacrum_engine import io_tools
from .render_object import RenderObject


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


class GLContext:

    def __init__(self) -> None:
        self.ctx = mgl.create_context(require=330)

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
        fragment_path: str,
        vertex_path: str | None = None,
        vao_args: list[str] | None = None,
        gl_buffer: Buffer | None = None
    ) -> RenderObject:
        fragment = io_tools.read_file_to_str(fragment_path)

        if vertex_path is not None:
            vertex = io_tools.read_file_to_str(vertex_path)
        else:
            vertex = None

        return RenderObject(
            self,
            fragment,
            vertex,
            vao_args=vao_args,
            gl_buffer=gl_buffer,
        )

    def pg_to_tex(self, surface: pyg.Surface) -> mgl.Texture:
        channels = 4
        texture = self.ctx.texture(surface.get_size(), channels)
        texture.filter = (mgl.NEAREST, mgl.NEAREST)
        texture.swizzle = "BGRA"
        texture.write(surface.get_view("1"))
        return texture

    def pg_to_tex_update(
        self,
        texture: mgl.Texture,
        surface: pyg.Surface,
    ) -> mgl.Texture:
        texture.write(surface.get_view("1"))
        return texture
