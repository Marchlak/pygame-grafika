import pygame
import os
import sys
from model.model import Model
from view.view import View
from controller.controller import Controller

pygame.init()

SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Paint super aplikacja")


def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)



def main():
    model = Model()
    view = View(screen)
    controller = Controller(model, view)
    try:
        icon_path = resource_path("resources/icon.png")
        icon_image = pygame.image.load(icon_path)
        pygame.display.set_icon(icon_image)
    except Exception as e:
        print("Brak ikonki")
    try:
        music_path = resource_path("resources/paint.mp3")
        pygame.mixer.music.load(music_path)
        pygame.mixer.music.play(-1)
    except Exception as e:
        print("Gdzie ta muza")

    running = True
    while running:
        running = controller.process_input()
        controller.update_view()

    pygame.quit()


if __name__ == "__main__":
    main()
