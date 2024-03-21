from __future__ import annotations
from typing import *
if TYPE_CHECKING:
    from .gl_context import GLContext

import moderngl as mgl
import pygame as pyg


Uniform = mgl.Uniform | mgl.Texture | pyg.Surface


class RenderObject:

    def __init__(
        self,
        gl_context: GLContext,
        fragment: str,
        vertex: str | None = None,
        use_default: bool = False,
        vao_args: list[str] | None = None,
        gl_buffer: mgl.Buffer | None = None,
    ) -> None:
        self.use_default = use_default
        self.gl_context = gl_context
        self._fragment = fragment
        self._vertex = vertex
        self.vao_args = vao_args if vao_args else ["2f 2f", "vert", "texcoord"]

        if not vertex:
            vertex = self.gl_context.default_vert

        self.program = self.gl_context.ctx.program(
            vertex_shader=vertex,
            fragment_shader=fragment,
        )

        if not gl_buffer:
            gl_buffer = self.gl_context.quad_buffer

        self.vao = self.gl_context.ctx.vertex_array(
            self.program,
            [(gl_buffer, *self.vao_args)],
        )

        self.temp_textures: list[mgl.Texture] = []

    def update(self, uniforms: dict[str, Uniform] | None = None) -> None:
        if uniforms is None:
            uniforms = {}

        texture_id = 0
        uniform_list = list(self.program)

        for uniform in uniforms:
            if uniform in uniform_list:
                if isinstance(uniforms[uniform], mgl.Texture):
                    cast(mgl.Texture, uniforms[uniform]).use(texture_id)
                    cast(mgl.Uniform, self.program[uniform]).value = texture_id
                    texture_id += 1
                else:
                    cast(mgl.Uniform, self.program[uniform]).value = uniforms[uniform]

    def render(
        self,
        dest: mgl.Framebuffer | None = None,
        uniforms: dict | None = None,
    ) -> None:
        if uniforms is None:
            uniforms = {}

        if dest is None:
            dest = self.gl_context.ctx.screen

        dest.use()

        uniforms = self.parse_uniforms(uniforms)
        self.update(uniforms)
        self.vao.render(mode=mgl.TRIANGLE_STRIP)

        for texture in self.temp_textures:
            texture.release()
        self.temp_textures = []

    def parse_uniforms(self, uniforms: dict[str, Uniform]) -> dict[str, Uniform]:
        for name, value in uniforms.items():
            if isinstance(value, pyg.Surface):
                texture = self.gl_context.pg_to_tex(value)
                uniforms[name] = texture
                self.temp_textures.append(texture)
        return uniforms
