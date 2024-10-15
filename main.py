import pygame
from model.model import Model
from view.view import View
from controller.controller import Controller

pygame.init()

SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Paint - MVC Architecture")

def main():
    model = Model()
    view = View(screen)
    controller = Controller(model, view)

    running = True
    while running:
        running = controller.process_input()
        controller.update_view()

    pygame.quit()

if __name__ == "__main__":
    main()

