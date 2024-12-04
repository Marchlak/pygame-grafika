import pygame
import moderngl
import numpy as np
import glm
from colorsys import hsv_to_rgb

class HSVConeView:
    def __init__(self, screen):
        self.screen = screen
        self.ctx = None
        self.program = None
        self.vao = None
        self.angle_x = 0.0
        self.angle_y = 0.0
        self.clock = pygame.time.Clock()
        self.proj = glm.perspective(glm.radians(60.0),
                                    self.screen.get_width() / self.screen.get_height(),
                                    0.1, 100.0)

        self.init_gl()

    def init_gl(self):
        self.ctx = moderngl.create_context()
        self.ctx.enable(moderngl.DEPTH_TEST)

        self.vertex_data, self.index_data = self.generate_hsv_cone_with_base(segments=60, layers=60)

        vbo = self.ctx.buffer(self.vertex_data.astype('f4').tobytes())
        ibo = self.ctx.buffer(self.index_data.astype('i4').tobytes())

        vertex_shader = '''
        #version 330 core

        in vec3 in_position;
        in vec3 in_color;
        out vec3 v_color;

        uniform mat4 mvp;

        void main() {
            gl_Position = mvp * vec4(in_position, 1.0);
            v_color = in_color;
        }
        '''

        fragment_shader = '''
        #version 330 core

        in vec3 v_color;
        out vec4 f_color;

        void main() {
            f_color = vec4(v_color, 1.0);
        }
        '''

        self.program = self.ctx.program(
            vertex_shader=vertex_shader,
            fragment_shader=fragment_shader
        )
        vao_content = [
            (vbo, '3f 3f', 'in_position', 'in_color'),
        ]

        self.vao = self.ctx.vertex_array(self.program, vao_content, ibo)

    def generate_hsv_cone_with_base(self, segments=60, layers=60):
        vertices = []
        indices = []

        for i in range(layers + 1):
            v = i / layers  
            radius = v

            for j in range(segments + 1):
                h = j / segments
                theta = h * 2 * np.pi  

                x = radius * np.cos(theta)
                y = radius * np.sin(theta)
                z = v  

                s = radius

                r, g, b = hsv_to_rgb(h, s, v)

                vertices.extend([x, y, z, r, g, b])

        apex_index = len(vertices) // 6

        r, g, b = hsv_to_rgb(0, 0, 0)
        vertices.extend([0.0, 0.0, 0.0, r, g, b])

        for i in range(layers):
            for j in range(segments):
                first = i * (segments + 1) + j
                second = first + segments + 1

                indices.extend([first, second, first + 1])
                indices.extend([second, second + 1, first + 1])

        base_center_index = len(vertices) // 6

        v = 1.0
        r, g, b = hsv_to_rgb(0, 0, v)
        vertices.extend([0.0, 0.0, v, r, g, b])

        base_vertices_indices = []
        for j in range(segments + 1):
            index = (layers) * (segments + 1) + j
            base_vertices_indices.append(index)

        for j in range(segments):
            first = base_vertices_indices[j]
            second = base_vertices_indices[j + 1]
            indices.extend([first, second, base_center_index])

        return np.array(vertices), np.array(indices)


    def draw(self, rotation_angles):
        self.angle_x = rotation_angles[0]
        self.angle_y = rotation_angles[1]

        self.ctx.clear(0.0, 0.0, 0.0, 1.0)

        model = glm.mat4(1.0)
        model = glm.rotate(model, self.angle_x, glm.vec3(1.0, 0.0, 0.0))
        model = glm.rotate(model, self.angle_y, glm.vec3(0.0, 1.0, 0.0))

        model = glm.scale(model, glm.vec3(1.2, 1.2, 1.2))

        model = glm.translate(model, glm.vec3(0.0, 0.8, 0.0))

        view = glm.translate(glm.mat4(1.0), glm.vec3(0.0, 0.0, -5.0))

        mvp = self.proj * view * model

        self.program['mvp'].write(mvp.to_bytes())

        self.vao.render()

        pygame.display.flip()
        self.clock.tick(60)

    def destroy(self):
        self.vao.release()
        self.program.release()
        self.ctx.release()

    def cleanup(self):
        pass

