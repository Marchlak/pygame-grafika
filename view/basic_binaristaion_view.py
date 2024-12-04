import pygame

from components.resource_path import resource_path
from components.rgb_sliders import RGBSliders
from components.slider import Slider
from components.text_input import TextInput


class BasicBinarisationView:
    def __init__(self, screen):
        self.screen = screen
        self.button_font = pygame.font.SysFont(None, 24)
        self.mode = "Binarisation"  # Nazwa trybu
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
            {
                "label": "Binarise",
                "rect": pygame.Rect(120, 10, 100, 40),
                "action": "binarise",
            },
        ]

        self.algorithms = [
            {
                "label": "Percent Black",
                "action": "percent_black",
                "rect": pygame.Rect(10, 60, 150, 40),
            },
            {
                "label": "Mean Iterative",
                "action": "mean_iterative",
                "rect": pygame.Rect(170, 60, 150, 40),
            },
            {
                "label": "Entropy",
                "action": "entropy",
                "rect": pygame.Rect(330, 60, 150, 40),
            },
            {
                "label": "Manual",
                "action": "manual",
                "rect": pygame.Rect(490, 60, 150, 40),
            },
            {"label": "Otsu", "action": "otsu", "rect": pygame.Rect(650, 60, 150, 40)},
            {
                "label": "Niblack",
                "action": "niblack",
                "rect": pygame.Rect(810, 60, 150, 40),
            },
            {
                "label": "Sauvola",
                "action": "sauvola",
                "rect": pygame.Rect(970, 60, 150, 40),
            },
            {
                "label": "Bernsen",
                "action": "bernsen",
                "rect": pygame.Rect(1130, 60, 150, 40),
            },
        ]

        self.percent_slider = Slider(10, 180, 200, 20, 1, 100, 50, "Percent")

        self.iterative_slider = Slider(10, 180, 200, 20, 1, 50, 10, "Iterations")

        self.threshold_slider = Slider(10, 180, 200, 20, 0, 255, 128, "Threshold")

        self.window_size_slider = Slider(20, 200, 200, 20, 3, 51, 15, "Window Size")

        self.k_niblack_slider = Slider(
            10, 400, 200, 20, -1.0, 0.0, -0.2, "k (Niblack)"
        )

        self.k_sauvola_slider = Slider(20, 300, 200, 20, 0.0, 1.0, 0.5, "k (Sauvola)")

        self.R_sauvola_slider = Slider(20, 500, 200, 20, 0, 255, 128, "R (Sauvola)")

        self.contrast_threshold_slider = Slider(
            20, 300, 200, 20, 0, 255, 15, "Contrast Threshold (Bernsen)"
        )

        self.current_algorithm = "percent_black"

        self.message = None
        self.message_font = pygame.font.SysFont(None, 20)

    def display_message(self, message):
        self.message = message


    def render(
        self,
        loaded_image=None,
        binarised_image=None,
        current_algorithm="percent_black",
        parameters=None,
    ):
        self.screen.fill((255, 255, 255))
        mouse_pos = pygame.mouse.get_pos()

        # Render głównych przycisków
        for button in self.buttons:
            is_hover = button["rect"].collidepoint(mouse_pos)
            text_color = (255, 255, 255)
            if is_hover:
                text_color = (0, 255, 0)
            rect_color = (128, 20, 40)
            pygame.draw.rect(self.screen, rect_color, button["rect"])
            text_surface = self.button_font.render(button["label"], True, text_color)
            text_rect = text_surface.get_rect(center=button["rect"].center)
            self.screen.blit(text_surface, text_rect)

        for algo in self.algorithms:
            is_hover = algo["rect"].collidepoint(mouse_pos)
            text_color = (0, 0, 0)
            if algo["action"] == current_algorithm:
                rect_color = (0, 255, 0)
            elif is_hover:
                rect_color = (200, 200, 200)
            else:
                rect_color = (150, 150, 150)
            pygame.draw.rect(self.screen, rect_color, algo["rect"])
            text_surface = self.button_font.render(algo["label"], True, text_color)
            text_rect = text_surface.get_rect(center=algo["rect"].center)
            self.screen.blit(text_surface, text_rect)

        if current_algorithm == "percent_black":
            self.percent_slider.draw(self.screen)
        elif current_algorithm == "mean_iterative":
            self.iterative_slider.draw(self.screen)
        elif current_algorithm == "manual":
            self.threshold_slider.draw(self.screen)
        elif current_algorithm == "entropy":
            pass  
        elif current_algorithm == "otsu":
            pass
        elif current_algorithm == "niblack":
            self.window_size_slider.draw(self.screen)
            self.k_niblack_slider.draw(self.screen)
        elif current_algorithm == "sauvola":
            self.window_size_slider.draw(self.screen)
            self.k_sauvola_slider.draw(self.screen)
            self.R_sauvola_slider.draw(self.screen)
        elif current_algorithm == "bernsen":
            self.window_size_slider.draw(self.screen)
            self.contrast_threshold_slider.draw(self.screen)

        if self.message:
            message_surface = self.message_font.render(self.message, True, (0, 0, 0))
            message_rect = message_surface.get_rect(center=(960, 20))
            self.screen.blit(message_surface, message_rect)


        if loaded_image:
            image_rect = loaded_image.get_rect(center=(960, 540))
            self.screen.blit(loaded_image, image_rect)

        if binarised_image:
            bin_rect = binarised_image.get_rect(center=(960, 540))
            self.screen.blit(binarised_image, bin_rect)

        pygame.display.flip()

    def get_button_action(self, mouse_pos):
        for button in self.buttons:
            if button["rect"].collidepoint(mouse_pos):
                return button["action"]
        for algo in self.algorithms:
            if algo["rect"].collidepoint(mouse_pos):
                return algo["action"]
        return None

    def handle_event(self, event):
        self.percent_slider.handle_event(event)
        self.iterative_slider.handle_event(event)
        self.threshold_slider.handle_event(event)
        self.window_size_slider.handle_event(event)
        self.k_niblack_slider.handle_event(event)
        self.k_sauvola_slider.handle_event(event)
        self.R_sauvola_slider.handle_event(event)
        self.contrast_threshold_slider.handle_event(event)
