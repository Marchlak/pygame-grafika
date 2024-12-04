from interfaces import IView
import pygame
from components.text_input import TextInput
from components.slider import Slider
from components.color_area import ColorArea

class ColorConversionView(IView):
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.Font(None, 36)
        self.input_font = pygame.font.Font(None, 28)
        self.exit_request = False

        start_x = 50
        start_y = 200
        spacing_y = 80

        self.rgb_inputs = {
            'R': TextInput(start_x + 150, start_y, 100, 40, self.input_font, text="0", max_length=3, input_type='int', min_value=0, max_value=255),
            'G': TextInput(start_x + 300, start_y, 100, 40, self.input_font, text="0", max_length=3, input_type='int', min_value=0, max_value=255),
            'B': TextInput(start_x + 450, start_y, 100, 40, self.input_font, text="0", max_length=3, input_type='int', min_value=0, max_value=255)
        }

        self.cmyk_inputs = {
            'C': TextInput(start_x + 150, start_y + spacing_y, 100, 40, self.input_font, text='0.0', max_length=5, input_type='float', min_value=0.0, max_value=100.0),
            'M': TextInput(start_x + 300, start_y + spacing_y, 100, 40, self.input_font, text='0.0', max_length=5, input_type='float', min_value=0.0, max_value=100.0),
            'Y': TextInput(start_x + 450, start_y + spacing_y, 100, 40, self.input_font, text='0.0', max_length=5, input_type='float', min_value=0.0, max_value=100.0),
            'K': TextInput(start_x + 600, start_y + spacing_y, 100, 40, self.input_font, text='100.0', max_length=5, input_type='float', min_value=0.0, max_value=100.0)
        }

        self.hsv_inputs = {
            'H': TextInput(start_x + 150, start_y + 2 * spacing_y, 100, 40, self.input_font, text='0', max_length=3, input_type='int', min_value=0, max_value=360),
            'S': TextInput(start_x + 300, start_y + 2 * spacing_y, 100, 40, self.input_font, text='0', max_length=3, input_type='int', min_value=0, max_value=100),
            'V': TextInput(start_x + 450, start_y + 2 * spacing_y, 100, 40, self.input_font, text='0', max_length=3, input_type='int', min_value=0, max_value=100)
        }

        self.buttons = [
            {"label": "Back", "rect": pygame.Rect(1800, 10, 80, 40), "action": "back_to_menu"},
        ]

        self.button_font = pygame.font.SysFont(None, 24)
        self.current_color = (0, 0, 0)

        self.slider_r = Slider(50, 900, 300, 20, 0, 255, 0, "R")

        self.color_area = ColorArea(50, 500, 300, "COLOR PANEL")

    def draw(self, color_data):

        self.screen.fill((255, 255, 255))

        self.current_color = color_data.get('rgb', (0, 0, 0))

        red = self.current_color[0]

        self.slider_r.draw(self.screen)

        self.color_area.draw(self.screen, red)

        color_rect = pygame.Rect(50, 50, 100, 100)
        pygame.draw.rect(self.screen, self.current_color, color_rect)

        label_color = (0, 0, 0)
        labels = [
            ('RGB:', 50, 200),
            ('CMYK:', 50, 200 + 80),
            ('HSV:', 50, 200 + 160)
        ]

        for text, x, y in labels:
            label = self.font.render(text, True, label_color)
            self.screen.blit(label, (x, y + 5))

        for key, input_box in self.rgb_inputs.items():
            input_box.draw(self.screen)
            label = self.input_font.render(key, True, label_color)
            self.screen.blit(label, (input_box.rect.x - 30, input_box.rect.y + 10))

        for key, input_box in self.cmyk_inputs.items():
            input_box.draw(self.screen)
            label = self.input_font.render(key, True, label_color)
            self.screen.blit(label, (input_box.rect.x - 30, input_box.rect.y + 10))

        for key, input_box in self.hsv_inputs.items():
            input_box.draw(self.screen)
            label = self.input_font.render(key, True, label_color)
            self.screen.blit(label, (input_box.rect.x - 30, input_box.rect.y + 10))

        for button in self.buttons:
            color = (0, 0, 255)
            pygame.draw.rect(self.screen, color, button["rect"])
            text_surface = self.button_font.render(button["label"], True, (255, 255, 255))
            self.screen.blit(text_surface, (button["rect"].x + 10, button["rect"].y + 10))

        pygame.display.flip()

    def get_rgb_values(self):
        try:
            r = int(self.rgb_inputs['R'].get_text())
            g = int(self.rgb_inputs['G'].get_text())
            b = int(self.rgb_inputs['B'].get_text())
            return [r, g, b]
        except ValueError:
            return [0, 0, 0]

    def get_hsv_values(self):
        try:
            h = int(self.hsv_inputs['H'].get_text())
            s = int(self.hsv_inputs['S'].get_text())
            v = int(self.hsv_inputs['V'].get_text())
            return [h, s, v]
        except ValueError:
            return [0, 0, 0]

    def get_cmyk_values(self):
        try:
            c = float(self.cmyk_inputs['C'].get_text())
            m = float(self.cmyk_inputs['M'].get_text())
            y = float(self.cmyk_inputs['Y'].get_text())
            k = float(self.cmyk_inputs['K'].get_text())
            return [c, m, y, k]
        except ValueError:
            return [0.0, 0.0, 0.0, 100.0]

    def set_rgb_values(self, values):
        self.rgb_inputs["R"].set_text(str(values[0]))
        self.rgb_inputs["G"].set_text(str(values[1]))
        self.rgb_inputs["B"].set_text(str(values[2]))

    def set_hsv_values(self, values):
        self.hsv_inputs["H"].set_text(str(values[0]))
        self.hsv_inputs["S"].set_text(str(values[1]))
        self.hsv_inputs["V"].set_text(str(values[2]))

    def set_cmyk_values(self, values):
        self.cmyk_inputs["C"].set_text(f"{values[0]:.2f}")
        self.cmyk_inputs["M"].set_text(f"{values[1]:.2f}")
        self.cmyk_inputs["Y"].set_text(f"{values[2]:.2f}")
        self.cmyk_inputs["K"].set_text(f"{values[3]:.2f}")

    def handle_event(self, event):
        self.slider_r.handle_event(event)

        self.color_area.handle_event(event)

        for input_box in self.rgb_inputs.values():
            input_box.handle_event(event)
        for input_box in self.cmyk_inputs.values():
            input_box.handle_event(event)
        for input_box in self.hsv_inputs.values():
            input_box.handle_event(event)

        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = event.pos
            self.check_button_click(mouse_pos)


    def check_button_click(self, pos):
        for button in self.buttons:
            if button["rect"].collidepoint(pos):
                if "action" in button and button["action"] == "back_to_menu":
                    self.exit_request = True

