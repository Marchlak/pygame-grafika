import pygame
import threading
from components.choose_file import choose_file

class AnalyzeController:
    def __init__(self, view, model):
        self.view = view
        self.model = model
        self.exit_request = False
        self.loaded_image = None
        self.analysis_results = {}
        self.binarization_results = {}
        self.segmentation_result = None

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
                    elif action == "analyze":
                        self.analyze_green()
                    elif action == "load_image":
                        self.execute()
                    elif action == "preprocess_image":
                        self.preprocess_image()
                    elif action == "binarize":
                        self.binarize_image()
                    elif action == "segment":
                        self.perform_segmentation()

        return True

    def analyze_green(self):
        if self.loaded_image:
            self.model.set_image(self.loaded_image)
            self.model.analyze_green()
            self.analysis_results = self.model.get_analysis_green_results()
            self.view.render(
                self.loaded_image,
                self.analysis_results,
                self.binarization_results,
                self.segmentation_result,
            )

    def preprocess_image(self):
        if self.loaded_image:
            self.model.set_image(self.loaded_image)
            self.model.preprocess_image()
            self.loaded_image = self.model.image_surface  # Update with preprocessed image
            self.view.set_loaded_image(self.loaded_image)
            self.view.render(
                self.loaded_image,
                self.analysis_results,
                self.binarization_results,
                self.segmentation_result,
            )

    def binarize_image(self):
        if self.loaded_image:
            self.model.set_image(self.loaded_image)
            self.model.automatic_binarization()
            self.binarization_results = self.model.get_binarization_results()
            processed_image = self.binarization_results.get("binarized_image")
            if processed_image:
                self.loaded_image = processed_image 
                self.view.set_loaded_image(self.loaded_image)
            self.view.render(
                self.loaded_image,
                self.analysis_results,
                self.binarization_results,
                self.segmentation_result,
            )

    def perform_segmentation(self):
        if self.loaded_image:
            self.model.set_image(self.loaded_image)
            self.model.image_segmentation()
            self.segmentation_result = self.model.get_segmentation_result()
            processed_image = self.segmentation_result
            if processed_image:
                self.loaded_image = processed_image
                self.view.set_loaded_image(self.loaded_image)
            self.view.render(
                self.loaded_image,
                self.analysis_results,
                self.binarization_results,
                self.segmentation_result,
            )

    def update_view(self):
        self.view.render(
            self.loaded_image,
            self.analysis_results,
            self.binarization_results,
            self.segmentation_result,
        )
        if self.model.last_message:
            self.view.display_message(self.model.last_message)

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
                    scale_factor = min(800 / width, 800 / height)
                    new_width = int(width * scale_factor)
                    new_height = int(height * scale_factor)
                    image = pygame.transform.smoothscale(image, (new_width, new_height))

                self.loaded_image = image
                self.view.set_loaded_image(self.loaded_image)

                self.view.render(
                    self.loaded_image,
                    self.analysis_results,
                    self.binarization_results,
                    self.segmentation_result,
                )

            except pygame.error as e:
                print(f"Failed to load image: {e}")

    def _show_error_message(self, message):
        self.view.display_message(message)
