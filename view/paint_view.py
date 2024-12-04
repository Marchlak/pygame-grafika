import pygame
import math
import os
import sys
from components.resource_path import resource_path


class PaintView:
    def __init__(self, screen):
        self.screen = screen
        self.button_font = pygame.font.SysFont(None, 24)
        self.buttons = [
            {"label": "Small", "rect": pygame.Rect(10, 10, 80, 40), "size": 3},
            {"label": "Medium", "rect": pygame.Rect(100, 10, 80, 40), "size": 6},
            {"label": "Large", "rect": pygame.Rect(190, 10, 80, 40), "size": 9},
            {"label": "Brush", "rect": pygame.Rect(280, 10, 80, 40), "mode": "brush"},
            {"label": "Rectangle", "rect": pygame.Rect(370, 10, 120, 40), "mode": "rectangle"},
            {"label": "Triangle", "rect": pygame.Rect(500, 10, 120, 40), "mode": "triangle"},
            {"label": "Ellipse", "rect": pygame.Rect(630, 10, 120, 40), "mode": "ellipse"},
            {"label": "Text", "rect": pygame.Rect(760, 10, 80, 40), "mode": "text"},
            {"label": "Line", "rect": pygame.Rect(850, 10, 80, 40), "mode": "line"},
            {"label": "Clear", "rect": pygame.Rect(940, 10, 80, 40), "action": "clear"},
            {"label": "Save", "rect": pygame.Rect(1030, 10, 80, 40), "action": "save"},
            {"label": "Back", "rect": pygame.Rect(1800, 10, 80, 40), "action": "back_to_menu"},
            ]
        self.color_palette_rect = pygame.Rect(1500, 10, 233, 40)
        self.current_color_rect = pygame.Rect(1400, 10, 80, 40)
        self.colors = self.generate_color_palette()

        nerd_image_path = resource_path("resources/nerd.png")
        self.nerd_image = pygame.image.load(nerd_image_path)
        self.nerd_image = pygame.transform.scale(self.nerd_image, (self.nerd_image.get_width() // 3, self.nerd_image.get_height() // 3))
        self.nerd_rect = self.nerd_image.get_rect(topleft=(1130, 10))
        self.show_tooltip = False



    def generate_color_palette(self):
        colors = []
        steps = self.color_palette_rect.width // 7

        for i in range(steps):
            value = int(255 * ((steps - i) / steps))
            colors.append((value, value, value))

        for i in range(steps):
            r = 255
            g = int(255 * (i / steps))
            b = 0
            colors.append((r, g, b))

        for i in range(steps):
            r = int(255 * ((steps - i) / steps))
            g = 255
            b = 0
            colors.append((r, g, b))

        for i in range(steps):
            r = 0
            g = 255
            b = int(255 * (i / steps))
            colors.append((r, g, b))

        for i in range(steps):
            r = 0
            g = int(255 * ((steps - i) / steps))
            b = 255
            colors.append((r, g, b))

        for i in range(steps):
            r = int(255 * (i / steps))
            g = 0
            b = 255
            colors.append((r, g, b))

        for i in range(steps):
            r = 255
            g = 0
            b = int(255 * ((steps - i) / steps))
            colors.append((r, g, b))

        return colors


    def is_color_palette_click(self, pos):
        return self.color_palette_rect.collidepoint(pos)

    def get_color_from_palette(self, pos):
        relative_x = pos[0] - self.color_palette_rect.x
        if 0 <= relative_x < self.color_palette_rect.width:
            color_index = int(relative_x * len(self.colors) / self.color_palette_rect.width)
            return self.colors[color_index]
        return (0, 0, 0)

    def is_hovering_nerd_image(self, pos):
        return self.nerd_rect.collidepoint(pos)


    def render(self, objects, current_line, current_sline, rectangle_object, triangle_object, ellipse_object, text_object, current_brush_size, current_color, font_size, drawing_mode):
        self.screen.fill((255, 255, 255))

        for obj in objects:
            if obj['type'] == 'line':
                if len(obj['points']) >= 2:
                    pygame.draw.lines(self.screen, obj['color'], False, obj['points'], obj['brush_size'])
            elif obj['type'] == 'rectangle':
                if obj['rectangle']:
                    self.draw_rectangle(obj['rectangle'], obj['color'])
            elif obj['type'] == 'triangle':
                if obj['triangle']:
                    self.draw_triangle(obj['triangle'], obj['color'])
            elif obj['type'] == 'ellipse':
                if obj['ellipse']:
                    self.draw_ellipse(obj['ellipse'], obj['color'])
            elif obj['type'] == 'text':
                if(obj['text']):
                    self.draw_text(obj['text'], obj['color'], obj['font_size'])
            elif obj['type'] == 'sline':
                if obj['sline']:
                    self.draw_line(obj['sline'], obj['color'], obj['brush_size'])


        if len(current_line) > 1:
            pygame.draw.lines(self.screen, current_color, False, current_line, current_brush_size)

        if rectangle_object and isinstance(rectangle_object, dict) and rectangle_object.get('start_pos'):
            self.draw_rectangle(rectangle_object, current_color)

        if current_sline and 'start_pos' in current_sline and 'end_pos' in current_sline:
            self.draw_line(current_sline, current_color, current_brush_size)

        if triangle_object and isinstance(triangle_object, dict) and triangle_object.get('start_pos'):
            self.draw_triangle(triangle_object, current_color)

        if ellipse_object and isinstance(ellipse_object, dict) and ellipse_object.get('start_pos'):
            self.draw_ellipse(ellipse_object, current_color)

        if text_object and 'text' in text_object:
            self.draw_text(text_object, current_color, font_size)


        for button in self.buttons:
            if 'mode' in button and button['mode'] == drawing_mode:
                color = (0, 255, 0)
            elif 'size' in button and button['size'] == current_brush_size:
                color = (0, 255, 0) 
            else:
                color = (0, 0, 255)

            pygame.draw.rect(self.screen, color, button["rect"])
            text_surface = self.button_font.render(button["label"], True, (255, 255, 255))
            self.screen.blit(text_surface, (button["rect"].x + 10, button["rect"].y + 10))

        for x, color in enumerate(self.colors):
            pygame.draw.line(self.screen, color, (self.color_palette_rect.x + x, self.color_palette_rect.y),
                             (self.color_palette_rect.x + x, self.color_palette_rect.y + self.color_palette_rect.height))

        pygame.draw.rect(self.screen, current_color, self.current_color_rect)

        self.screen.blit(self.nerd_image, self.nerd_rect)

        if self.show_tooltip:
            tooltip_text = "Witam drogiego użytkownika :). Kształty rysujesz przeciągając myszką. Ruszasz ostatnim obiektem za pomocą jkil. Rotujesz za pomocą R. Skalujesz za pomocą A i S. Aplikacja ma super architekture mvc. I jest napisana w najlepszym języku programowania. Posiada spełnione 5 punktów na ocene 5. A nawet więcej. Życzę miłego dzionka."
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


    def draw_rectangle(self, rectangle, color):
        start_pos = rectangle['start_pos']
        width = rectangle['width']
        height = rectangle['height']
        angle = rectangle['angle']
        scale = rectangle['scale']

        if width < 0:
            start_pos = (start_pos[0] + width, start_pos[1])
            width = abs(width)
        if height < 0:
            start_pos = (start_pos[0], start_pos[1] + height)
            height = abs(height)

        rect = pygame.Rect(start_pos[0], start_pos[1], width * scale, height * scale)

        temp_surface = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)
        temp_surface.fill(color)

        rotated_surface = pygame.transform.rotate(temp_surface, angle)
        rotated_rect = rotated_surface.get_rect(center=rect.center)

        self.screen.blit(rotated_surface, rotated_rect.topleft)


    def rotate_points(self, points, angle, center):
        angle_rad = math.radians(angle)
        rotated_points = []

        for point in points:
            x_shifted = point[0] - center[0]
            y_shifted = point[1] - center[1]

            x_rotated = x_shifted * math.cos(angle_rad) - y_shifted * math.sin(angle_rad)
            y_rotated = x_shifted * math.sin(angle_rad) + y_shifted * math.cos(angle_rad)

            x_final = x_rotated + center[0]
            y_final = y_rotated + center[1]

            rotated_points.append((x_final, y_final))

        return rotated_points



    def draw_triangle(self, triangle, color):
        start_pos = triangle['start_pos']
        width = triangle['width']
        height = triangle['height']
        scale = triangle['scale']
        angle = triangle['angle']

        point1 = (start_pos[0], start_pos[1])
        point2 = (start_pos[0] + width * scale, start_pos[1] + height * scale)
        point3 = (start_pos[0] + width * scale / 2, start_pos[1] - height * scale)

        points = [point1, point2, point3]

        rotated_points = self.rotate_points(points, angle, point1)

        pygame.draw.polygon(self.screen, color, rotated_points)

    def draw_ellipse(self, ellipse, color):
        start_pos = ellipse['start_pos']
        width = ellipse['width']
        height = ellipse['height']
        scale = ellipse['scale']
        angle = ellipse['angle']

        if width < 0:
            start_pos = (start_pos[0] + width, start_pos[1])
            width = abs(width)
        if height < 0:
            start_pos = (start_pos[0], start_pos[1] + height)
            height = abs(height)


        rect = pygame.Rect(start_pos[0], start_pos[1], width * scale, height * scale)

        temp_surface = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)
        pygame.draw.ellipse(temp_surface, color, (0, 0, rect.width, rect.height))

        rotated_surface = pygame.transform.rotate(temp_surface, angle)
        rotated_rect = rotated_surface.get_rect(center=rect.center)

        self.screen.blit(rotated_surface, rotated_rect.topleft)

    def draw_text(self, text_object, color, font_size):
        font = pygame.font.SysFont(None, font_size)
        text_surface = font.render(text_object['text'], True, color)
        self.screen.blit(text_surface, text_object['start_pos'])

    def draw_line(self, line, color, brush_size):
        pygame.draw.line(self.screen, color, line['start_pos'], line['end_pos'], brush_size)
