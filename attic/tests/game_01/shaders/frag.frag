#version 330

uniform sampler2D surface;
uniform sampler2D ui_surf;

out vec4 f_color;
in vec2 uv;

void main() {
    f_color = vec4(texture(surface, uv).rgb, 1.0);

    vec4 ui_color = texture(ui_surf, uv);
    if (ui_color.a > 0) {
        f_color = ui_color;
    }
}
