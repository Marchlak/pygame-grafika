import pygame


class AnalyzeView:
    def __init__(self, screen):
        self.screen = screen
        self.button_font = pygame.font.SysFont(None, 24)
        self.result_font = pygame.font.SysFont(None, 24)
        self.buttons = [
            {
                "label": "Load Image",
                "rect": pygame.Rect(10, 10, 100, 40),
                "action": "load_image",
            },
            {
                "label": "Preprocess",
                "rect": pygame.Rect(120, 10, 100, 40),
                "action": "preprocess_image",
            },
            {
                "label": "Binarize",
                "rect": pygame.Rect(230, 10, 100, 40),
                "action": "binarize",
            },
            {
                "label": "Segment",
                "rect": pygame.Rect(340, 10, 100, 40),
                "action": "segment",
            },
            {
                "label": "Analyze",
                "rect": pygame.Rect(450, 10, 100, 40),
                "action": "analyze",
            },
            {
                "label": "Back",
                "rect": pygame.Rect(560, 10, 80, 40),
                "action": "back_to_menu",
            },
        ]
        self.loaded_image = None
        self.binarized_image = None
        self.segmented_image = None
        self.message = None
        self.message_font = pygame.font.SysFont(None, 20)


    def set_loaded_image(self, image):
        self.loaded_image = image

    def render(
        self,
        loaded_image=None,
        analysis_results=None,
        binarization_results=None,
        segmentation_result=None,
    ):
        self.screen.fill((255, 255, 255))
        mouse_pos = pygame.mouse.get_pos()
        for button in self.buttons:
            is_hover = button["rect"].collidepoint(mouse_pos)
            text_color = (255, 255, 255)
            if is_hover:
                text_color = (0, 255, 0)
            rect_color = (128, 20, 40)
            pygame.draw.rect(self.screen, rect_color, button["rect"])
            text_surface = self.button_font.render(button["label"], True, text_color)
            text_rect = text_surface.get_rect(center=button["rect"].center)
            self.screen.blit(text_surface, text_rect)

        if self.loaded_image:
            image_rect = self.loaded_image.get_rect(center=(960, 540))
            self.screen.blit(self.loaded_image, image_rect)

        if analysis_results:
            self.display_results(analysis_results)

        if self.message:
            message_surface = self.message_font.render(self.message, True, (0, 0, 0))
            message_rect = message_surface.get_rect(center=(960, 60))
            self.screen.blit(message_surface, message_rect)

        pygame.display.flip()

    def display_message(self, message):
        self.message = message

    def display_results(self, results):
        green_pct = results.get("green_percentage", 0.0)
        largest_area = results.get("largest_green_area", 0)
        largest_pct = results.get("largest_green_percentage", 0.0)

        base_x = 10
        base_y = 60
        line_spacing = 30

        green_text = f"Green Pixels: {green_pct:.2f}%"
        green_surface = self.result_font.render(green_text, True, (0, 128, 0))
        self.screen.blit(green_surface, (base_x, base_y))

        area_text = f"Largest Green Area: {largest_area} pixels ({largest_pct:.2f}%)"
        area_surface = self.result_font.render(area_text, True, (0, 128, 0))
        self.screen.blit(area_surface, (base_x, base_y + line_spacing))

    def get_button_action(self, mouse_pos):
        for button in self.buttons:
            if button["rect"].collidepoint(mouse_pos):
                return button["action"]
        return None

    def handle_event(self, event):
        pass

