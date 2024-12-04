# filter_controller.py

import pygame
import threading
from tkinter import Tk
from tkinter.filedialog import askopenfilename
import numpy as np
import pygame.surfarray as surfarray
from components.choose_file import choose_file

class FilterController:
    def __init__(self, view):
        self.view = view
        self.exit_request = False
        self.loaded_image = None
        self.adjusted_image = None
        self.mode = "Add/Subtract" 

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
                if self.loaded_image:
                    self.apply_rgb_adjustments()
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
                    elif action == "toggle_mode":
                        self.view.toggle_mode()
                        self.mode = self.view.mode
                        if self.loaded_image:
                            self.apply_rgb_adjustments()
                    elif action.startswith("grayscale_"):
                        self.view.set_grayscale_method(action)
                        if self.loaded_image:
                            self.apply_rgb_adjustments()
        return True

    def update_view(self):
        self.view.render(self.adjusted_image)

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
                self.apply_rgb_adjustments()
            except pygame.error as e:
                print(f"Nie udało się załadować obrazu: {e}")

    def apply_rgb_adjustments(self):
        if self.loaded_image:
            r_adjust, g_adjust, b_adjust = self.view.get_rgb_values()
            brightness = self.view.get_brightness_value()
            grayscale_method = self.view.get_grayscale_method()
            grayscale_intensity = self.view.get_grayscale_intensity()

            array = surfarray.array3d(self.loaded_image).astype(
                np.int16
            ) 

            if self.mode == "Add/Subtract":
                array[:, :, 0] += r_adjust
                array[:, :, 1] += g_adjust
                array[:, :, 2] += b_adjust
                array += brightness
                np.clip(array, 0, 255, out=array)
            elif self.mode == "Multiply/Divide":
                r_factor = (
                    1 + (r_adjust / 255.0)
                    if r_adjust >= 0
                    else 1 / (1 + abs(r_adjust) / 255.0)
                )
                g_factor = (
                    1 + (g_adjust / 255.0)
                    if g_adjust >= 0
                    else 1 / (1 + abs(g_adjust) / 255.0)
                )
                b_factor = (
                    1 + (b_adjust / 255.0)
                    if b_adjust >= 0
                    else 1 / (1 + abs(b_adjust) / 255.0)
                )

                array[:, :, 0] = array[:, :, 0] * r_factor
                array[:, :, 1] = array[:, :, 1] * g_factor
                array[:, :, 2] = array[:, :, 2] * b_factor

                array += brightness

                np.clip(array, 0, 255, out=array)

            if grayscale_method:
                intensity = grayscale_intensity / 255.0

                if grayscale_method == "grayscale_average":
                    grayscale = (array[:, :, 0] + array[:, :, 1] + array[:, :, 2]) / 3.0
                elif grayscale_method == "grayscale_r":
                    grayscale = array[:, :, 0]
                elif grayscale_method == "grayscale_g":
                    grayscale = array[:, :, 1]
                elif grayscale_method == "grayscale_b":
                    grayscale = array[:, :, 2]
                elif grayscale_method == "grayscale_avg_rg":
                    grayscale = (array[:, :, 0] + array[:, :, 1]) / 2.0
                elif grayscale_method == "grayscale_max_rgb":
                    grayscale = np.maximum(np.maximum(array[:, :, 0], array[:, :, 1]), array[:, :, 2])
                elif grayscale_method == "grayscale_min_rgb":
                    grayscale = np.minimum(np.minimum(array[:, :, 0], array[:, :, 1]), array[:, :, 2])
                else:
                    grayscale = array[:, :, 0]

                grayscale = np.stack([grayscale]*3, axis=-1)

                array = array * (1 - intensity) + grayscale * intensity

                np.clip(array, 0, 255, out=array)

            array = array.astype("uint8")

            adjusted_surface = surfarray.make_surface(array)

            if self.loaded_image.get_masks()[3] != 0:
                alpha = surfarray.array_alpha(self.loaded_image)
                adjusted_surface = adjusted_surface.convert_alpha()
                surfarray.pixels_alpha(adjusted_surface)[:] = alpha
            else:
                adjusted_surface = adjusted_surface.convert()

            self.adjusted_image = adjusted_surface

