import pygame

class ColorArea:
    def __init__(self, x, y, size, label):
        self.rect = pygame.Rect(x, y, size, size)
        self.size = size
        self.selected_pos = (0, size - 1)
        self.label = label
        self.font = pygame.font.Font(None, 24)
        self.r = 0
        self.g = 0
        self.b = 0

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                x = max(0, min(event.pos[0] - self.rect.x, self.size - 1))
                y = max(0, min(event.pos[1] - self.rect.y, self.size - 1))
                self.selected_pos = (x, y)
                self.g = int((x / (self.size - 1)) * 255)
                self.b = int(((self.size - 1 - y) / (self.size - 1)) * 255)
                return True
        return False

    def get_values(self):
        return self.g, self.b

    def draw(self, screen, red):
        for x in range(self.size):
            for y in range(self.size):
                g = int((x / (self.size - 1)) * 255)
                b = int(((self.size - 1 - y) / (self.size - 1)) * 255)
                color = (red, g, b)
                screen.set_at((self.rect.x + x, self.rect.y + y), color)
        pygame.draw.rect(screen, (255, 255, 255), (self.rect.x + self.selected_pos[0] - 5,
                                                 self.rect.y + self.selected_pos[1] - 5, 10, 10), 2)
        label_surf = self.font.render(self.label, True, (0, 0, 0))
        screen.blit(label_surf, (self.rect.x, self.rect.y - 30))

    def set_selected_pos_based_on_gb(self, g, b):
        x = int((g / 255) * (self.size - 1))
        y = int(((self.size - 1) - (b / 255) * (self.size - 1)))
        self.selected_pos = (x, y)
        self.g = g
        self.b = b

