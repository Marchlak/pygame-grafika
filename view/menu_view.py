import pygame
from components.resource_path import resource_path

class MenuView:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.Font(None, 36)
        margin_top = 20
        margin = 77
        self.buttons = [
            {"label": "Paint", "rect": pygame.Rect(860, margin_top + margin * 0, 250, 60), "action": "start_paint"},
            {"label": "Cube", "rect": pygame.Rect(860, margin_top + margin * 1, 250, 60), "action": "figure"},
            {"label": "Cone", "rect": pygame.Rect(860, margin_top + margin * 2, 250, 60), "action": "cone"},
            {"label": "Color Change", "rect": pygame.Rect(860, margin_top + margin * 3, 250, 60), "action": "color"},
            {"label": "Image Loader", "rect": pygame.Rect(860, margin_top + margin * 4, 250, 60), "action": "image"},
            {"label": "A Filter", "rect": pygame.Rect(860, margin_top + margin * 5, 250, 60), "action": "filter"},
            {"label": "B Filter", "rect": pygame.Rect(860, margin_top + margin * 6, 250, 60), "action": "bfilter"},
            {"label": "Histogram", "rect": pygame.Rect(860, margin_top + margin * 7, 250, 60), "action": "histogram"},
            {"label": "Basic Binarisation", "rect": pygame.Rect(860, margin_top + margin * 8, 250, 60), "action": "bbin"},
            {"label": "Bezier", "rect": pygame.Rect(860, margin_top + margin * 9, 250, 60), "action": "bezier"},
            {"label": "Analyze", "rect": pygame.Rect(860, margin_top + margin * 10, 250, 60), "action": "analyze"},
            {"label": "Project", "rect": pygame.Rect(860, margin_top + margin * 11, 250, 60), "action": "project"},
            {"label": "Exit", "rect": pygame.Rect(860, margin_top + margin * 12, 250, 60), "action": "exit"},
        ]

        nerd_image_path = resource_path("resources/nerd2.png")
        self.nerd_image = pygame.image.load(nerd_image_path)
        self.nerd_image = pygame.transform.scale(self.nerd_image, (self.nerd_image.get_width(), self.nerd_image.get_height()))
        self.nerd_rect = self.nerd_image.get_rect(topleft=(1550, 750))
        self.show_tooltip = False

        background_path = resource_path("resources/menu_dalle.png")
        self.background = pygame.image.load(background_path).convert()
        self.background = pygame.transform.scale(self.background, (1920, 1080))


    def draw(self):
        self.screen.blit(self.background, (0, 0))

        mouse_pos = pygame.mouse.get_pos()

        for button in self.buttons:
            is_hover = button["rect"].collidepoint(mouse_pos)
            text_color = (255,255,255)
            if is_hover:
                text_color = (0,255,0)
            pygame.draw.rect(self.screen, (0, 128, 255), button["rect"])
            text_surface = self.font.render(button["label"], True, text_color)
            text_rect = text_surface.get_rect(center=button["rect"].center)
            self.screen.blit(text_surface, text_rect)
            self.screen.blit(self.nerd_image, self.nerd_rect)

        if self.show_tooltip:
            tooltip_text = "Wszystkie wymagania z zadania 5. zostały spełniona na ocene 5"
            tooltip_font = pygame.font.SysFont(None, 20)
            lines = tooltip_text.split('.')
            lines = [line.strip() for line in lines if line.strip()]
            tooltip_width = max(tooltip_font.size(line)[0] for line in lines) + 20
            tooltip_height = tooltip_font.get_height() * len(lines) + 10

            pygame.draw.rect(self.screen, (255, 255, 200), (self.nerd_rect.left, self.nerd_rect.top - self.nerd_image.get_height() //2, tooltip_width, tooltip_height))

            for i, line in enumerate(lines):
                tooltip_surface = tooltip_font.render(line, True, (0, 0, 0))
                self.screen.blit(tooltip_surface, (self.nerd_rect.left + 10, (self.nerd_rect.top - self.nerd_image.get_height() //2) + (i * tooltip_font.get_height())))


        pygame.display.flip()


    def get_button_action(self, mouse_pos):
        for button in self.buttons:
            if button["rect"].collidepoint(mouse_pos):
                return button["action"]


    def is_hovering_nerd_image(self, pos):
        return self.nerd_rect.collidepoint(pos)
        return None

