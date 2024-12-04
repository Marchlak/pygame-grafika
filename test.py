import pygame
import moderngl
import numpy as np
import sys
import glm  # Requires the PyGLM package

def main():
    # Initialize Pygame and create an OpenGL-enabled window
    pygame.init()
    pygame.display.set_caption('Rotating RGB Cube')
    SCREEN_WIDTH = 800
    SCREEN_HEIGHT = 600
    pygame.display.gl_set_attribute(pygame.GL_CONTEXT_MAJOR_VERSION, 3)
    pygame.display.gl_set_attribute(pygame.GL_CONTEXT_MINOR_VERSION, 3)
    pygame.display.gl_set_attribute(pygame.GL_CONTEXT_PROFILE_MASK, pygame.GL_CONTEXT_PROFILE_CORE)
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.OPENGL | pygame.DOUBLEBUF)

    # Create a ModernGL context
    ctx = moderngl.create_context()

    # Define cube vertices and colors
    vertices = np.array([
        # positions       # colors (R, G, B)
        -1, -1, -1,      0,   0,   0,     # 0
         1, -1, -1,    255,   0,   0,     # 1
         1,  1, -1,    255, 255,   0,     # 2
        -1,  1, -1,      0, 255,   0,     # 3
        -1, -1,  1,      0,   0, 255,     # 4
         1, -1,  1,    255,   0, 255,     # 5
         1,  1,  1,    255, 255, 255,     # 6
        -1,  1,  1,      0, 255, 255      # 7
    ], dtype='f4')

    # Define the indices of the cube's faces
    indices = np.array([
        0, 1, 2, 2, 3, 0,  # Back face
        4, 5, 6, 6, 7, 4,  # Front face
        1, 5, 6, 6, 2, 1,  # Right face
        0, 4, 7, 7, 3, 0,  # Left face
        3, 2, 6, 6, 7, 3,  # Top face
        0, 1, 5, 5, 4, 0   # Bottom face
    ], dtype='i4')

    # Create vertex buffer and index buffer
    vbo = ctx.buffer(vertices.tobytes())
    ibo = ctx.buffer(indices.tobytes())

    # Create shaders
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

    # Compile the shader program
    program = ctx.program(
        vertex_shader=vertex_shader,
        fragment_shader=fragment_shader
    )

    # Define the format of the buffer content
    vao_content = [
        (vbo, '3f 3f', 'in_position', 'in_color'),
    ]

    # Create vertex array object
    vao = ctx.vertex_array(program, vao_content, ibo)

    # Set up the projection matrix
    proj = glm.perspective(glm.radians(60.0), SCREEN_WIDTH / SCREEN_HEIGHT, 0.1, 100.0)

    # Initial rotation angles
    angle_x = 0.0
    angle_y = 0.0

    # Enable depth testing
    ctx.enable(moderngl.DEPTH_TEST)

    clock = pygame.time.Clock()
    running = True
    while running:
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Clear the screen
        ctx.clear(0.0, 0.0, 0.0)

        # Update rotation angles
        angle_x += 0.5
        angle_y += 0.5

        # Create model, view, and mvp matrices
        model = glm.rotate(glm.mat4(1.0), glm.radians(angle_x), glm.vec3(1.0, 0.0, 0.0))
        model = glm.rotate(model, glm.radians(angle_y), glm.vec3(0.0, 1.0, 0.0))

        view = glm.translate(glm.mat4(1.0), glm.vec3(0.0, 0.0, -6.0))

        mvp = proj * view * model

        # Pass the mvp matrix to the shader
        program['mvp'].write(mvp.to_bytes())

        # Render the cube
        vao.render()

        # Swap buffers
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()

if __name__ == '__main__':
    main()

