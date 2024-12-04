import pygame

class Slider:
    def __init__(self, x, y, width, height, min_val, max_val, initial_val, label):
        self.rect = pygame.Rect(x, y, width, height)
        self.min = min_val
        self.max = max_val
        self.value = initial_val
        self.handle_radius = height // 2
        self.handle_pos = self.get_handle_pos()
        self.dragging = False
        self.label = label
        self.font = pygame.font.Font(None, 24)

    def get_handle_pos(self):
        ratio = (self.value - self.min) / (self.max - self.min)
        return (self.rect.x + int(ratio * self.rect.width), self.rect.y + self.rect.height // 2)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.handle_rect().collidepoint(event.pos):
                self.dragging = True
        elif event.type == pygame.MOUSEBUTTONUP:
            self.dragging = False
        elif event.type == pygame.MOUSEMOTION:
            if self.dragging:
                x = max(self.rect.x, min(event.pos[0], self.rect.x + self.rect.width))
                ratio = (x - self.rect.x) / self.rect.width
                self.value = int(self.min + ratio * (self.max - self.min))
                self.handle_pos = self.get_handle_pos()

    def handle_rect(self):
        return pygame.Rect(
            self.handle_pos[0] - self.handle_radius,
            self.handle_pos[1] - self.handle_radius,
            self.handle_radius * 2,
            self.handle_radius * 2
        )

    def set_value(self, new_value):
        self.value = max(self.min, min(new_value, self.max))
        self.handle_pos = self.get_handle_pos()

    def draw(self, screen):
        pygame.draw.line(screen, (0, 0, 0), (self.rect.x, self.rect.y + self.rect.height // 2),
                         (self.rect.x + self.rect.width, self.rect.y + self.rect.height // 2), 2)
        pygame.draw.circle(screen, (255, 0, 0), self.handle_pos, self.handle_radius)
        label_surf = self.font.render(f"{self.label}: {self.value}", True, (0, 0, 0))
        screen.blit(label_surf, (self.rect.x, self.rect.y - 30))

