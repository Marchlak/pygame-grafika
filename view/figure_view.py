import pygame
import moderngl
import numpy as np
import glm

class FigureView:
    def __init__(self, screen):
        self.screen = screen
        self.ctx = None
        self.program = None
        self.vao = None
        self.angle_x = 0.0
        self.angle_y = 0.0
        self.clock = pygame.time.Clock()
        self.proj = glm.perspective(glm.radians(60.0), self.screen.get_width() / self.screen.get_height(), 0.1, 100.0)

        self.init_gl()


    def init_gl(self):
        self.ctx = moderngl.create_context()
        self.ctx.enable(moderngl.DEPTH_TEST)

        vertices = np.array([
            -1, -1, -1,      0,   0,   0,
             1, -1, -1,    255,   0,   0,
             1,  1, -1,    255, 255,   0,
            -1,  1, -1,      0, 255,   0,
            -1, -1,  1,      0,   0, 255,
             1, -1,  1,    255,   0, 255,
             1,  1,  1,    255, 255, 255,     
            -1,  1,  1,      0, 255, 255    
        ], dtype='f4')

        indices = np.array([
            0, 1, 2, 2, 3, 0,
            4, 5, 6, 6, 7, 4,
            1, 5, 6, 6, 2, 1,
            0, 4, 7, 7, 3, 0,
            3, 2, 6, 6, 7, 3,
            0, 1, 5, 5, 4, 0   
        ], dtype='i4')

        vbo = self.ctx.buffer(vertices.tobytes())
        ibo = self.ctx.buffer(indices.tobytes())

        vertex_shader = '''
        #version 330 core

        in vec3 in_position;
        in vec3 in_color;
        out vec3 v_color;

        uniform mat4 mvp;

        void main() {
            gl_Position = mvp * vec4(in_position, 1.0);
            v_color = in_color / 255.0;
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

    def draw(self, rotation_angles):
        self.angle_x = rotation_angles[0]
        self.angle_y = rotation_angles[1]

        self.ctx.clear(0.0, 0.0, 0.0, 1.0)

        model = glm.rotate(glm.mat4(1.0), self.angle_x, glm.vec3(1.0, 0.0, 0.0))
        model = glm.rotate(model, self.angle_y, glm.vec3(0.0, 1.0, 0.0))

        view = glm.translate(glm.mat4(1.0), glm.vec3(0.0, 0.0, -6.0))

        mvp = self.proj * view * model

        self.program['mvp'].write(mvp.to_bytes())

        self.vao.render()

        pygame.display.flip()
        self.clock.tick(60)



    def destroy(self):
        self.vao.release()
        self.program.release()
        self.ctx.release()


