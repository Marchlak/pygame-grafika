import pygame
from components.resource_path import resource_path
from components.rgb_sliders import RGBSliders
from components.slider import Slider

class HistogramView:
    def __init__(self, screen):
        self.screen = screen
        self.button_font = pygame.font.SysFont(None, 24)
        self.mode = "Add/Subtract"  # Domyślny tryb
        self.buttons = [
            {
                "label": "Load Image",
                "rect": pygame.Rect(10, 10, 100, 40),
                "action": "load_image",
            },
            {
                "label": "Back",
                "rect": pygame.Rect(1800, 10, 80, 40),
                "action": "back_to_menu",
            },
        ]

    def render(self, loaded_image=None):
        self.screen.fill((255, 255, 255))
        mouse_pos = pygame.mouse.get_pos()
        for button in self.buttons:
            is_hover = button["rect"].collidepoint(mouse_pos)
            text_color = (255,255,255)
            if is_hover:
                text_color = (0,255,0)
            rect_color = (128, 20, 40)
            pygame.draw.rect(self.screen, rect_color, button["rect"])
            text_surface = self.button_font.render(
                button["label"], True, text_color
            )
            text_rect = text_surface.get_rect(center=button["rect"].center)
            self.screen.blit(text_surface, text_rect)


        if loaded_image:
            image_rect = loaded_image.get_rect(center=(960, 540))
            self.screen.blit(loaded_image, image_rect)

        pygame.display.flip()

    def get_button_action(self, mouse_pos):
        for button in self.buttons:
            if button["rect"].collidepoint(mouse_pos):
                return button["action"]
        return None

    def handle_event(self, event):
        pass
