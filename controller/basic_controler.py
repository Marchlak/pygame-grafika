# filter_controller.py

import pygame
import threading
from tkinter import Tk
from tkinter.filedialog import askopenfilename
import numpy as np
import pygame.surfarray as surfarray
from components.choose_file import choose_file

class HistogramController:
    def __init__(self, view):
        self.view = view
        self.exit_request = False
        self.loaded_image = None

    def process_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type in (
                pygame.MOUSEBUTTONDOWN,
                pygame.MOUSEBUTTONUP,
                pygame.MOUSEMOTION,
            ):
                self.view.handle_event(event)
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.exit_request = True

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos
                action = self.view.get_button_action(mouse_pos)
                if action:
                    if action == "back_to_menu":
                        self.exit_request = True
                    elif action == "load_image":
                        self.execute()
        return True

    def update_view(self):
        self.view.render(self.loaded_image)

    def execute(self):
        thread = threading.Thread(target=self._choose_file_thread, daemon=True)
        thread.start()

    def _choose_file_thread(self):
        file_path = choose_file()
        if file_path:
            try:
                image = pygame.image.load(file_path).convert_alpha()
                width, height = image.get_size()
                if width > 800 or height > 800:
                    self._show_error_message("Obraz jest zbyt duży. Maksymalny rozmiar to 800x800 pikseli.")
                    return

                self.loaded_image = image
            except pygame.error as e:
                print(f"Nie udało się załadować obrazu: {e}")
