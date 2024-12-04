import pygame
import threading
import numpy as np
import pygame.surfarray as surfarray
from components.choose_file import choose_file
from components.text_input import TextInput
from components.slider import Slider


class BasicBinarisationController:
    def __init__(self, view, model):
        self.model = model
        self.view = view
        self.exit_request = False
        self.loaded_image = None
        self.binarised_image = None
        self.current_algorithm = "percent_black"
        self.parameters = {"percent": 50, "max_iterations": 10, "threshold": 128}

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
                        self.execute_load_image()
                    elif action == "binarise":
                        self.execute_binarisation()
                    elif action in [
                        "percent_black",
                        "mean_iterative",
                        "entropy",
                        "manual",
                        "otsu",
                        "niblack",
                        "sauvola",
                        "bernsen",
                    ]:
                        self.current_algorithm = action
        return True

    def update_view(self):
        self.view.render(
            self.loaded_image,
            self.binarised_image,
            self.current_algorithm,
            self.parameters,
        )

    def execute_load_image(self):
        thread = threading.Thread(target=self._choose_file_thread, daemon=True)
        thread.start()

    def _choose_file_thread(self):
        file_path = choose_file()
        if file_path:
            try:
                image = pygame.image.load(file_path).convert_alpha()
                width, height = image.get_size()
                if width > 800 or height > 800:
                    self._show_error_message(
                        "Obraz jest zbyt duży. Maksymalny rozmiar to 800x800 pikseli."
                    )
                    return

                self.loaded_image = image
                self.binarised_image = None  #
            except pygame.error as e:
                self.view.display_message(f"Nie udało się załadować obrazu: {e}")

    def execute_binarisation(self):
        self.parameters["percent"] = self.view.percent_slider.value
        self.parameters["max_iterations"] = self.view.iterative_slider.value
        self.parameters["threshold"] = self.view.threshold_slider.value
        self.parameters["window_size"] = self.view.window_size_slider.value
        self.parameters["k_niblack"] = self.view.k_niblack_slider.value
        self.parameters["k_sauvola"] = self.view.k_sauvola_slider.value
        self.parameters["R_sauvola"] = self.view.R_sauvola_slider.value
        self.parameters["contrast_threshold"] = self.view.contrast_threshold_slider.value
        if self.loaded_image is None:
            self._show_error_message("Najpierw załaduj obraz.")
            return
        thread = threading.Thread(target=self._binarise_thread, daemon=True)
        thread.start()

    def _binarise_thread(self):
        if self.current_algorithm == "percent_black":
            percent = self.parameters.get("percent", 50)
            self.binarised_image = self.model.percent_black_selection(
                self.loaded_image, percent=percent
            )
        elif self.current_algorithm == "mean_iterative":
            max_iterations = self.parameters.get("max_iterations", 10)
            self.binarised_image = self.model.mean_iterative_selection(
                self.loaded_image, max_iterations=max_iterations
            )
        elif self.current_algorithm == "entropy":
            self.binarised_image = self.model.entropy_selection(self.loaded_image)
        elif self.current_algorithm == "manual":
            threshold = self.parameters.get("threshold", 128)
            self.binarised_image = self.model.manual_threshold(
                self.loaded_image, threshold=threshold
            )
        elif self.current_algorithm == "otsu":
            self.binarised_image = self.model.otsu_threshold(self.loaded_image)
        elif self.current_algorithm == "niblack":
            window_size = self.parameters.get("window_size", 15)
            k = self.parameters.get("k_niblack", -0.2)
            self.binarised_image = self.model.niblack_threshold(
                self.loaded_image, window_size=window_size, k=k
            )
        elif self.current_algorithm == "sauvola":
            window_size = self.parameters.get("window_size", 15)
            k = self.parameters.get("k_sauvola", 0.5)
            R = self.parameters.get("R_sauvola", 128)
            self.binarised_image = self.model.sauvola_threshold(
                self.loaded_image, window_size=window_size, k=k, R=R
            )
        elif self.current_algorithm == "bernsen":
            window_size = self.parameters.get("window_size", 15)
            contrast_threshold = self.parameters.get("contrast_threshold", 15)
            self.binarised_image = self.model.bernsen_threshold(
                self.loaded_image, window_size=window_size, contrast_threshold=contrast_threshold
            )
        else:
            self._show_error_message("Nieznany algorytm binaryzacji.")

    def _show_error_message(self, message):
        self.view.display_message(f"Error: {message}")

    def get_parameters(self):
        return self.parameters

    def set_parameter(self, key, value):
        self.parameters[key] = value
