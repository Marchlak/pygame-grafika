import pygame
import numpy as np
import time
import os
from components.resource_path import resource_path

class ImageView:
    def __init__(self, screen):
        self.screen = screen
        self.image_surface = None
        self.image_rect = pygame.Rect(100, 100, 1780, 780)

        self.font = pygame.font.Font(None, 36)
        self.buttons = [
            {
                "label": "Save Image",
                "rect": pygame.Rect(630, 920, 200, 60),
                "action": "save_image",
            },
            {
                "label": "Load Image",
                "rect": pygame.Rect(850, 920, 200, 60),
                "action": "load_image",
            },
            {
                "label": "Back to Menu",
                "rect": pygame.Rect(1070, 920, 200, 60),
                "action": "back_to_menu",
            },
        ]

        self.min_width = 200
        self.min_height = 150
        self.max_width = self.image_rect.width
        self.max_height = self.image_rect.height

        self.message = ""
        self.loading_time = None

        nerd_image_path = resource_path("resources/nerd-dog.png")
        self.nerd_image = pygame.image.load(nerd_image_path)
        self.nerd_image = pygame.transform.scale(self.nerd_image, (self.nerd_image.get_width() // 5, self.nerd_image.get_height() // 5))
        self.nerd_rect = self.nerd_image.get_rect(topleft=(100, 10))
        self.show_tooltip = False


    def set_loading_time(self, loading_time):
        self.loading_time = loading_time

    def open_file_dialog(self):
        import tkinter as tk
        from tkinter import filedialog

        root = tk.Tk()
        root.withdraw()

        file_path = filedialog.askopenfilename(
            title="Wybierz plik PPM",
            filetypes=[("PPM files", "*.ppm"), ("All files", "*.*")]
        )
        root.destroy()
        return file_path

    def set_message(self, message):
        self.message = message

    def update_image(self, model):
        width, height = model.width, model.height
        pixels = model.pixels
        maxval = model.maxval
        img_format = model.format

        if img_format in ["P1", "P4"]:
            rgb_pixels = np.where(pixels == 0, 255, 0).astype(np.uint8)
            rgb_image = np.stack((rgb_pixels,) * 3, axis=-1)

        elif img_format in ["P2", "P5"]:
            gray_pixels = (pixels / maxval * 255).astype(np.uint8)
            rgb_image = np.stack((gray_pixels,) * 3, axis=-1)

        elif img_format in ["P3", "P6"]:
            rgb_pixels = (pixels / maxval * 255).astype(np.uint8)
            rgb_image = rgb_pixels

        else:
            raise ValueError("Unsupported image format")

        rgb_image = np.transpose(rgb_image, (1, 0, 2))

        try:
            image_surface = pygame.surfarray.make_surface(rgb_image)
        except ValueError as e:
            raise ValueError(f"Failed to create Pygame surface: {e}")

        original_width, original_height = image_surface.get_size()

        scale_w = self.image_rect.width / original_width
        scale_h = self.image_rect.height / original_height
        scale = min(scale_w, scale_h)

        scaled_width = int(original_width * scale)
        scaled_height = int(original_height * scale)

        if scaled_width < self.min_width or scaled_height < self.min_height:
            scale = max(self.min_width / original_width, self.min_height / original_height)
            scaled_width = int(original_width * scale)
            scaled_height = int(original_height * scale)

            if scaled_width > self.max_width or scaled_height > self.max_height:
                scale = min(self.max_width / original_width, self.max_height / original_height)
                scaled_width = int(original_width * scale)
                scaled_height = int(original_height * scale)

        scaled_width = min(scaled_width, self.max_width)
        scaled_height = min(scaled_height, self.max_height)

        image_surface = pygame.transform.scale(image_surface, (scaled_width, scaled_height))

        final_surface = pygame.Surface((self.image_rect.width, self.image_rect.height))
        final_surface.fill((0, 0, 0))

        pos_x = (self.image_rect.width - scaled_width) // 2
        pos_y = (self.image_rect.height - scaled_height) // 2

        final_surface.blit(image_surface, (pos_x, pos_y))

        self.image_surface = final_surface

    def draw(self):
        self.screen.fill((0, 0, 0))

        if self.image_surface:
            self.screen.blit(self.image_surface, self.image_rect)
        else:
            font = pygame.font.Font(None, 36)
            text_surface = font.render("No image loaded.", True, (255, 255, 255))
            text_rect = text_surface.get_rect(center=(self.screen.get_width() // 2
            ,self.screen.get_height() //2))
            self.screen.blit(text_surface, text_rect)

        for button in self.buttons:
            pygame.draw.rect(self.screen, (0, 128, 255), button["rect"])
            text_surface = self.font.render(button["label"], True, (255, 255, 255))
            text_rect = text_surface.get_rect(center=button["rect"].center)
            self.screen.blit(text_surface, text_rect)

        current_time = time.strftime("%H:%M:%S")
        time_surface = self.font.render(f"Current Time: {current_time}", True, (255, 255, 255))
        padding = 20
        time_rect = time_surface.get_rect(topright=(self.screen.get_width() - padding, padding))
        self.screen.blit(time_surface, time_rect)

        if hasattr(self, 'loading_time') and self.loading_time is not None:
            loading_time_text = f"Loading Time: {self.loading_time:.2f} seconds"
            loading_time_surface = self.font.render(loading_time_text, True, (255, 255, 255))
            loading_time_rect = loading_time_surface.get_rect(topright=(self.screen.get_width() - padding, padding + 40))
            self.screen.blit(loading_time_surface, loading_time_rect)

        if self.message:
            message_surface = self.font.render(self.message, True, (255, 255, 255))
            message_rect = message_surface.get_rect(center=(self.screen.get_width() // 2, 50))
            self.screen.blit(message_surface, message_rect)

        self.screen.blit(self.nerd_image, self.nerd_rect)

        if self.show_tooltip:
            tooltip_text = "Witam drogiego użytkownika :). Wszystkie wymagania zostały spełnione. Da się bez problemu wczytać każdy obraz testowy. Jest obsługa komentarzy. Da się spowrotem zapisać każdy wczytany obraz. brak użycia bibliotek. Wszystko dzieje się asynchronicznie z kolejką i wzorcem command. Następnym razem lepiej byłoby żeby pliki testowe były w formacie utf-8 który jest bardziej uniwersalny. Miłego dzionka i pozdrawiam"
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

    def is_hovering_nerd_image(self, pos):
        return self.nerd_rect.collidepoint(pos)

    def get_button_action(self, mouse_pos):
        for button in self.buttons:
            if button["rect"].collidepoint(mouse_pos):
                return button["action"]
        return None

