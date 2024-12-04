import pygame as pg
import moderngl as mgl
from camera import Camera
from light import Light
from mesh import Mesh
from scene import Scene
from scene_renderer import SceneRenderer

class GraphicsEngine:
    def __init__(self, screen):
        self.screen = screen
        self.WIN_SIZE = self.screen.get_size()
        pg.event.set_grab(True)
        pg.mouse.set_visible(False)
        self.ctx = mgl.create_context()
        self.ctx.enable(flags=mgl.DEPTH_TEST | mgl.CULL_FACE)
        self.clock = pg.time.Clock()
        self.time = 0
        self.delta_time = self.clock.tick(60)
        self.light = Light()
        self.camera = Camera(self)
        self.mesh = Mesh(self)
        self.scene = Scene(self)
        self.scene_renderer = SceneRenderer(self)
        self.exit_request = False

    def process_input(self):
        for event in pg.event.get():
            if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                self.exit_request = True

    def update_view(self):
        self.get_time()
        self.camera.update()
        self.render()
        self.delta_time = self.clock.tick(60) / 1000.0  

    def get_time(self):
        self.time = pg.time.get_ticks() * 0.001

    def render(self):
        self.ctx.clear(color=(0.08, 0.16, 0.18))
        self.scene_renderer.render()
        pg.display.flip()

    def cleanup(self):
        self.mesh.destroy()
        self.scene_renderer.destroy()
        pg.mouse.set_visible(True)
        pg.event.set_grab(False)

