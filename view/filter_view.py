import pygame
from components.resource_path import resource_path
from components.rgb_sliders import RGBSliders
from components.slider import Slider

class FilterView:
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
                "label": f"Mode: {self.mode}",
                "rect": pygame.Rect(120, 10, 200, 40),
                "action": "toggle_mode",
            },
            {
                "label": "Back",
                "rect": pygame.Rect(1800, 10, 80, 40),
                "action": "back_to_menu",
            },
        ]
        self.rgb_sliders = RGBSliders(x=10, y=100, width=300, height=20, spacing=60)
        self.brightness_slider = Slider(
            x=10,
            y=100 + 3 * 60 + 40,  
            width=300,
            height=20,
            min_val=-255,
            max_val=255,
            initial_val=0,
            label='Brightness'
        )
        self.grayscale_methods = [
            ("Average", "grayscale_average"),
            ("Red", "grayscale_r"),
            ("Green", "grayscale_g"),
            ("Blue", "grayscale_b"),
            ("Average RG", "grayscale_avg_rg"),
            ("Max RGB", "grayscale_max_rgb"),
            ("Min RGB", "grayscale_min_rgb"),
        ]

        start_x = 10
        start_y = 320 + 60
        button_width = 200
        button_height = 30
        spacing = 40
        for i, (label, action) in enumerate(self.grayscale_methods):
            button = {
                "label": f"Grayscale: {label}",
                "rect": pygame.Rect(start_x, start_y + i * (button_height + spacing), button_width, button_height),
                "action": action,
            }
            self.buttons.append(button)

        self.grayscale_intensity_slider = Slider(
            x=300,
            y=start_y,
            width=300,
            height=20,
            min_val=0,
            max_val=255,
            initial_val=0,
            label='Grayscale Intensity'
        )
        self.current_grayscale_method = None

    def render(self, loaded_image=None):
        self.screen.fill((255, 255, 255))
        mouse_pos = pygame.mouse.get_pos()
        for button in self.buttons:
            is_hover = button["rect"].collidepoint(mouse_pos)
            text_color = (255,255,255)
            if is_hover:
                text_color = (0,255,0)
            rect_color = (128, 20, 40)
            if self.current_grayscale_method == button["action"]:
                rect_color = (128,128,255)

            pygame.draw.rect(self.screen, rect_color, button["rect"])
            text_surface = self.button_font.render(
                button["label"], True, text_color
            )
            text_rect = text_surface.get_rect(center=button["rect"].center)
            self.screen.blit(text_surface, text_rect)

        self.rgb_sliders.draw(self.screen)

        self.brightness_slider.draw(self.screen)

        self.grayscale_intensity_slider.draw(self.screen)

        if loaded_image:
            image_rect = loaded_image.get_rect(center=(960, 540))
            self.screen.blit(loaded_image, image_rect)

        pygame.display.flip()

    def get_button_action(self, mouse_pos):
        for button in self.buttons:
            if button["rect"].collidepoint(mouse_pos):
                return button["action"]
        return None

    def get_rgb_values(self):
        return self.rgb_sliders.get_values()

    def get_brightness_value(self):
        return self.brightness_slider.value

    def get_grayscale_intensity(self):
        return self.grayscale_intensity_slider.value

    def handle_event(self, event):
        self.rgb_sliders.handle_event(event)
        self.brightness_slider.handle_event(event)
        self.grayscale_intensity_slider.handle_event(event)

    def toggle_mode(self):
        if self.mode == "Add/Subtract":
            self.mode = "Multiply/Divide"
        else:
            self.mode = "Add/Subtract"
        for button in self.buttons:
            if button["action"] == "toggle_mode":
                button["label"] = f"Mode: {self.mode}"
                break

    def set_grayscale_method(self, method):
        self.current_grayscale_method = method

    def get_grayscale_method(self):
        return self.current_grayscale_method
