# filter_controller.py

import pygame
import threading
import numpy as np
import pygame.surfarray as surfarray
from model.filter_model import FilterModel
from components.choose_file import choose_file

class BFilterController:
    def __init__(self, view):
        self.view = view
        self.exit_request = False
        self.loaded_image = None
        self.filter_model = FilterModel()

    def process_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            else:
                self.view.handle_event(event)

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.exit_request = True

            if event.type == pygame.MOUSEMOTION:
                if self.view.is_hovering_nerd_image(event.pos):
                    self.view.show_tooltip = True
                else:
                    self.view.show_tooltip = False


            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos
                action = self.view.get_button_action(mouse_pos)
                if action:
                    if action == "back_to_menu":
                        self.exit_request = True
                    elif action == "load_image":
                        self.execute()
                    elif action == "apply_smoothing":
                        self.apply_smoothing_filter()
                    elif action == "apply_median":
                        self.apply_median_filter()
                    elif action == "apply_sobel":
                        self.apply_sobel_filter()
                    elif action == "apply_high_pass":
                        self.apply_high_pass_filter()
                    elif action == "apply_gaussian_blur":
                        self.apply_gaussian_blur_filter()
                    elif action == "apply_custom_convolution":
                        self.apply_custom_convolution()
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
                self.loaded_image = image
                self.view.display_message(f"Obraz załadowany: {file_path}")
            except pygame.error as e:
                self.view.display_message(f"Nie udało się załadować obrazu: {e}")

    def apply_smoothing_filter(self):
        if self.loaded_image:
            self.view.display_message("Stosowanie filtru wygładzającego...")
            self.loaded_image = self.filter_model.apply_smoothing_filter(self.loaded_image)
            self.view.display_message("Filtr wygładzający zastosowany.")
        else:
            self.view.display_message("Nie wczytano żadnego obrazu.")

    def apply_median_filter(self):
        if self.loaded_image:
            self.view.display_message("Stosowanie filtru medianowego...")
            self.loaded_image = self.filter_model.apply_median_filter_numpy(self.loaded_image)
            self.view.display_message("Filtr medianowy zastosowany.")
        else:
            self.view.display_message("Nie wczytano żadnego obrazu.")

    def apply_sobel_filter(self):
        if self.loaded_image:
            self.view.display_message("Stosowanie filtru Sobela (wykrywanie krawędzi)...")
            self.loaded_image = self.filter_model.apply_sobel_filter_numpy(self.loaded_image)
            self.view.display_message("Filtr Sobela zastosowany.")
        else:
            self.view.display_message("Nie wczytano żadnego obrazu.")

    def apply_high_pass_filter(self):
        if self.loaded_image:
            self.view.display_message("Stosowanie filtru górnoprzepustowego (wyostrzającego)...")
            self.loaded_image = self.filter_model.apply_high_pass_filter_numpy(self.loaded_image)
            self.view.display_message("Filtr górnoprzepustowy zastosowany.")
        else:
            self.view.display_message("Nie wczytano żadnego obrazu.")

    def apply_gaussian_blur_filter(self):
        if self.loaded_image:
            self.view.display_message("Stosowanie filtru rozmycia gaussowskiego...")
            self.loaded_image = self.filter_model.apply_gaussian_blur_numpy(
                self.loaded_image, kernel_size=5, sigma=1.0
            )
            self.view.display_message("Filtr rozmycia gaussowskiego zastosowany.")
        else:
            self.view.display_message("Nie wczytano żadnego obrazu.")


    def apply_custom_convolution(self):
        if self.loaded_image:
            kernel_values = self.view.kernel_grid.get_kernel_values()
            kernel_size = self.view.kernel_grid.kernel_size
            kernel_array = np.array(kernel_values, dtype=np.float32)
            self.loaded_image = self.filter_model.apply_custom_convolution(
                self.loaded_image, kernel_array
            )
            self.view.display_message("Niestandardowy Filtr zastosowany")
        else:
            self.view.display_message("Nie wczytano żadnego obrazu.")

