import pygame
from components.slider import Slider

class RGBSliders:
    def __init__(self, x, y, width, height, spacing=50):
        self.sliders = {
            'Red': Slider(x, y, width, height, -255, 255, 0, 'Red'),
            'Green': Slider(x, y + spacing, width, height, -255, 255, 0, 'Green'),
            'Blue': Slider(x, y + 2 * spacing, width, height, -255, 255, 0, 'Blue')
        }

    def handle_event(self, event):
        for slider in self.sliders.values():
            slider.handle_event(event)

    def draw(self, screen):
        for slider in self.sliders.values():
            slider.draw(screen)

    def get_values(self):
        return (
            self.sliders['Red'].value,
            self.sliders['Green'].value,
            self.sliders['Blue'].value
        )

