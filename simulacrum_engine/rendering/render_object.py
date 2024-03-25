from __future__ import annotations
from typing import *
if TYPE_CHECKING:
    from .gl_context import GLContext

import moderngl as mgl
import pygame as pyg


Uniform = mgl.Uniform | mgl.Texture | pyg.Surface
UT = TypeVar("UT", bound=Uniform, covariant=True)


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

        # Use the ModernGL `Context` to instantiate a `Program`, which represents fully
        # processed executable OpenGL code. The `Program` can be passed to a
        # `VertexArray` for rendering.
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

    def render(
        self,
        *,
        buffer: mgl.Framebuffer | None = None,
        uniforms: dict[str, UT] | None = None,
    ) -> None:
        if uniforms is None:
            uniforms = {}

        if buffer is None:
            buffer = self.gl_context.ctx.screen
        buffer.use()

        # Convert PyGame `Surface` objects to ModernGL `Texture` instances.
        uniforms = self.parse_uniforms(uniforms=uniforms)

        # Run an update cycle.
        self.update(uniforms)

        # Render to the `VertexArray`.
        self.vao.render(mode=mgl.TRIANGLE_STRIP)

        # Free the textures we created so we're not leaking memory.
        for texture in self.temp_textures:
            texture.release()
        self.temp_textures = []

    def update(self, uniforms: dict[str, Uniform] | None = None) -> None:
        if uniforms is None:
            uniforms = {}

        texture_id = 0
        uniform_list = list(self.program)

        # Where `uniform` can be `mgl.Uniform | mgl.Texture`. All PyGame `Surface`
        # instances have been converted and added to a texture list to be freed after
        # the current render cycle.
        for uniform in uniforms:
            if uniform in uniform_list:
                if isinstance(uniforms[uniform], mgl.Texture):
                    cast(mgl.Texture, uniforms[uniform]).use(texture_id)
                    cast(mgl.Uniform, self.program[uniform]).value = texture_id
                    texture_id += 1
                else:
                    cast(mgl.Uniform, self.program[uniform]).value = uniforms[uniform]

    def parse_uniforms(self, *, uniforms: dict[str, UT]) -> dict[str, UT]:
        """
        Take in a mapping to `mgl.Uniform | mgl.Texture | pyg.Surface` types and check
        each value. If the value is type PyGame `Surface`, use the `GLContext` to
        convert it to a ModernGL `Texture` and add it to the temp textures list.

        The `Surface` object is passed to the GL Context where the `pg_to_tex` method
        calls `get_view`, returning a PyGame `BufferProxy`. This proxy is written to
        a new ModernGL `Texture` instance, and the original `Surface` is replaced by
        this new `Texture` in the passed uniforms dict.
        """
        for name, value in uniforms.items():
            if isinstance(value, pyg.Surface):
                texture = self.gl_context.pg_to_tex(surface=value)
                uniforms[name] = texture
                self.temp_textures.append(texture)
        return uniforms
