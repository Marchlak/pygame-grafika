# view/bezier_view.py

import pygame
import numpy as np
import math
from components.resource_path import resource_path

class BezierView:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.Font(None, 24)
        self.control_point_radius = 5
        self.move_handle_radius = 7
        self.message = None
        self.message_font = pygame.font.SysFont(None, 20)
        nerd_image_path = resource_path("resources/nerd.png")
        self.nerd_image = pygame.image.load(nerd_image_path)
        self.nerd_image = pygame.transform.scale(self.nerd_image, (self.nerd_image.get_width() // 3, self.nerd_image.get_height() // 3))
        self.nerd_rect = self.nerd_image.get_rect(topleft=(1130, 10))
        self.show_tooltip = False


    def display_message(self, message):
        self.message = message


    def draw(self, curves, current_control_points, move_handle_pos=None, current_mode='bezier'):
        if self.message:
            message_surface = self.message_font.render(self.message, True, (0, 0, 0))
            message_rect = message_surface.get_rect(center=(960, 20))
            self.screen.blit(message_surface, message_rect)

        for curve in curves:
            points = curve['points']
            mode = curve['mode']
            if mode == 'bezier':
                self.draw_bezier_curve(points)
            elif mode == 'polygon':
                self.draw_polygon(points)

        self.screen.blit(self.nerd_image, self.nerd_rect)

        if self.show_tooltip:
            tooltip_text = "Witam drogiego uzytkownika. Wszystkie podpunkty na ocene 5 zostały spełnione. Jest skalowanie rotacja i przesuwanie. Guzikami jak i myszką. Przesuwasz łapąc za środek. obracasz lewym przyciskiem myszy. Powiększasz i zmniejszasz scrollem. Przycisk mode zmienia z wielokątu na bezier"
            tooltip_font = pygame.font.SysFont(None, 20)
            lines = tooltip_text.split('.')
            lines = [line.strip() for line in lines if line.strip()]
            tooltip_width = max(tooltip_font.size(line)[0] for line in lines) + 20
            tooltip_height = tooltip_font.get_height() * len(lines) + 10

            pygame.draw.rect(self.screen, (255, 255, 200), (self.nerd_rect.left, self.nerd_rect.bottom + 5, tooltip_width, tooltip_height))

            for i, line in enumerate(lines):
                tooltip_surface = tooltip_font.render(line, True, (0, 0, 0))
                self.screen.blit(tooltip_surface, (self.nerd_rect.left + 10, self.nerd_rect.bottom + 10 + i * tooltip_font.get_height()))



        if current_control_points:
            for i, point in enumerate(current_control_points):
                pygame.draw.circle(self.screen, (255, 0, 0), (int(point[0]), int(point[1])), self.control_point_radius)
                label = self.font.render(f"P{i}", True, (0, 0, 0))
                self.screen.blit(label, (point[0] + 10, point[1]))

            if len(current_control_points) > 1:
                if current_mode == 'bezier':
                    pygame.draw.lines(self.screen, (0, 255, 0), False, current_control_points, 1)
                    bezier_points = self.compute_bezier_points(current_control_points)
                    pygame.draw.lines(self.screen, (0, 0, 255), False, bezier_points, 2)
                elif current_mode == 'polygon':
                    self.draw_polygon(current_control_points, is_current=True)

            if move_handle_pos:
                pygame.draw.circle(
                    self.screen,
                    (255, 165, 0),
                    (int(move_handle_pos[0]), int(move_handle_pos[1])),
                    self.move_handle_radius
                )


    def draw_bezier_curve(self, control_points):
        if len(control_points) > 1:
            bezier_points = self.compute_bezier_points(control_points)
            pygame.draw.lines(self.screen, (0, 0, 255), False, bezier_points, 2)
            pygame.draw.lines(self.screen, (0, 255, 0), False, control_points, 1)
            for i, point in enumerate(control_points):
                pygame.draw.circle(self.screen, (255, 0, 0), (int(point[0]), int(point[1])), self.control_point_radius)
                label = self.font.render(f"P{i}", True, (0, 0, 0))
                self.screen.blit(label, (point[0] + 10, point[1]))

    def draw_polygon(self, points, is_current=False):
        if len(points) >= 3:
            pygame.draw.polygon(self.screen, (0, 255, 0), points)
        elif len(points) >= 2:
            pygame.draw.lines(self.screen, (0, 255, 0), True, points, 2)

        for i, point in enumerate(points):
            pygame.draw.circle(self.screen, (255, 0, 0), (int(point[0]), int(point[1])), self.control_point_radius)
            label = self.font.render(f"P{i}", True, (0, 0, 0))
            self.screen.blit(label, (point[0] + 10, point[1]))

        if is_current and len(points) >= 3:
            centroid = self.get_centroid(points)
            pygame.draw.circle(
                self.screen,
                (255, 165, 0),
                (int(centroid[0]), int(centroid[1])),
                self.move_handle_radius
            )

    def compute_bezier_points(self, control_points, num_points=100):
        n = len(control_points) - 1
        t_values = np.linspace(0, 1, num_points)
        points = []

        for t in t_values:
            point = [0, 0]
            for i, cp in enumerate(control_points):
                bernstein = self.bernstein_poly(i, n, t)
                point[0] += cp[0] * bernstein
                point[1] += cp[1] * bernstein
            points.append((int(point[0]), int(point[1])))
        return points

    def bernstein_poly(self, i, n, t):
        return self.binomial_coeff(n, i) * (t ** i) * ((1 - t) ** (n - i))

    def binomial_coeff(self, n, k):
        from math import comb
        return comb(n, k)

    def get_centroid(self, points):
        x_sum = sum(point[0] for point in points)
        y_sum = sum(point[1] for point in points)
        n = len(points)
        return (x_sum / n, y_sum / n)

    def is_hovering_nerd_image(self, pos):
        return self.nerd_rect.collidepoint(pos)

