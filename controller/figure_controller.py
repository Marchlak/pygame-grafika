import pygame

class FigureController:
    def __init__(self, model, view):
        self.model = model
        self.view = view
        self.rotation_angle = [0.0, 0.0, 0.0]
        self.running = True
        self.exit_request = False

    def process_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                return False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                    self.exit_request = True
                    return True

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.rotation_angle[1] -= 0.05
        if keys[pygame.K_RIGHT]:
            self.rotation_angle[1] += 0.05
        if keys[pygame.K_UP]:
            self.rotation_angle[0] -= 0.05
        if keys[pygame.K_DOWN]:
            self.rotation_angle[0] += 0.05

        return True

    def update_view(self):
        self.view.draw(self.rotation_angle)

    def cleanup(self):
        pass
