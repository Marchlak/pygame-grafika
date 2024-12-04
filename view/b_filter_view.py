# b_filter_view.py

import pygame
from components.resource_path import resource_path
from components.rgb_sliders import RGBSliders
from components.slider import Slider
from components.text_input import TextInput
from components.kernel_input_grid import KernelInputGrid  # Import the KernelInputGrid
import numpy as np

class BFilterView:
    def __init__(self, screen):
        self.screen = screen
        self.button_font = pygame.font.SysFont(None, 24)
        self.mode = "Add/Subtract"
        self.buttons = [
            {
                "label": "Load Image",
                "rect": pygame.Rect(10, 10, 100, 40),
                "action": "load_image",
            },
            {
                "label": "Apply Smoothing",
                "rect": pygame.Rect(120, 10, 150, 40),
                "action": "apply_smoothing",
            },
            {
                "label": "Apply Median Filter",
                "rect": pygame.Rect(280, 10, 150, 40),
                "action": "apply_median",
            },
            {
                "label": "Apply Sobel Filter",
                "rect": pygame.Rect(440, 10, 150, 40),
                "action": "apply_sobel",
            },
            {
                "label": "Apply High Pass Filter",
                "rect": pygame.Rect(600, 10, 220, 40),
                "action": "apply_high_pass",
            },
            {
                "label": "Apply Gaussian Blur",
                "rect": pygame.Rect(830, 10, 220, 40),
                "action": "apply_gaussian_blur",
            },
            {
                "label": "Apply Custom Convolution",
                "rect": pygame.Rect(1060, 10, 220, 40),
                "action": "apply_custom_convolution",
            },
            {
                "label": "Back",
                "rect": pygame.Rect(1800, 10, 80, 40),
                "action": "back_to_menu",
            },
        ]

        self.kernel_size_input = TextInput(
            x=50, y=70, width=100, height=30, font=self.button_font,
            text='3', placeholder='Kernel Size', max_length=1,
            input_type='int', min_value=2, max_value=9
        )

        self.kernel_grid = KernelInputGrid(
            x=50, y=110, cell_size=50, font=self.button_font, kernel_size=3
        )
        self.message = None
        self.message_font = pygame.font.SysFont(None, 20)

        nerd_image_path = resource_path("resources/nerd.png")
        self.nerd_image = pygame.image.load(nerd_image_path)
        self.nerd_image = pygame.transform.scale(self.nerd_image, (self.nerd_image.get_width() // 3, self.nerd_image.get_height() // 3))
        self.nerd_rect = self.nerd_image.get_rect(topleft=(1450, 10))
        self.show_tooltip = False



    def display_message(self, message):
        self.message = message

    def render(self, loaded_image=None):
        self.screen.fill((255, 255, 255))

        mouse_pos = pygame.mouse.get_pos()
        for button in self.buttons:
            is_hover = button["rect"].collidepoint(mouse_pos)

            pygame.draw.rect(self.screen, (128, 20, 40), button["rect"])
            
            text_color = (255,255,255)
            
            if is_hover:
                text_color = (0,255,0)
            else:
                text_color = (255, 255, 255)

            text_surface = self.button_font.render(
                button["label"], True, text_color
            )
            text_rect = text_surface.get_rect(center=button["rect"].center)
            self.screen.blit(text_surface, text_rect)

        if loaded_image:
            image_rect = loaded_image.get_rect(center=(960, 540))
            self.screen.blit(loaded_image, image_rect)

        if self.message:
            message_surface = self.message_font.render(self.message, True, (0, 0, 0))
            message_rect = message_surface.get_rect(center=(960, 60))
            self.screen.blit(message_surface, message_rect)

        self.kernel_size_input.draw(self.screen)

        self.kernel_grid.draw(self.screen)

        self.screen.blit(self.nerd_image, self.nerd_rect)

        if self.show_tooltip:
            tooltip_text = "Witam drogiego użytkownika :). Żeby poprawić wygląd jabłuszka trzeba zastosować filtr medianowy. Do 3 pierwszych filtrów zostały przeprowadzone testy jednostkowe. Które są w pliku test_filter_model.py. Uruchamiamy je za pomocą python3 test_filter_model.py"
            tooltip_font = pygame.font.SysFont(None, 20)
            lines = tooltip_text.split('.')
            lines = [line.strip() for line in lines if line.strip()]
            tooltip_width = max(tooltip_font.size(line)[0] for line in lines) + 20
            tooltip_height = tooltip_font.get_height() * len(lines) + 10

            pygame.draw.rect(self.screen, (255, 255, 200), (self.nerd_rect.left, self.nerd_rect.bottom + 5, tooltip_width, tooltip_height))

            for i, line in enumerate(lines):
                tooltip_surface = tooltip_font.render(line, True, (0, 0, 0))
                self.screen.blit(tooltip_surface, (self.nerd_rect.left + 10, self.nerd_rect.bottom + 10 + i * tooltip_font.get_height()))


        pygame.display.flip()

    def get_button_action(self, mouse_pos):
        for button in self.buttons:
            if button["rect"].collidepoint(mouse_pos):
                return button["action"]
        return None

    def is_hovering_nerd_image(self, pos):
        return self.nerd_rect.collidepoint(pos)

    def handle_event(self, event):
        self.kernel_size_input.handle_event(event)

        new_kernel_size = int(self.kernel_size_input.get_text())
        if new_kernel_size != self.kernel_grid.kernel_size:
            self.kernel_grid.set_kernel_size(new_kernel_size)
            print(f"Kernel size updated to: {new_kernel_size}")

        self.kernel_grid.handle_event(event)

    def update(self):
        self.kernel_size_input.update()

        self.kernel_grid.update()
