import pygame
import os
import sys
from controller.menu_controller import MenuController
from model.color_model import ColorModel
from view.color_conversion_view import ColorConversionView
from controller.color_conversion_controller import ColorConversionController
from di_container import DIContainer
from components.resource_path import resource_path

def main():
    pygame.init()
    SCREEN_WIDTH = 1920
    SCREEN_HEIGHT = 1080
    pygame.display.set_caption("Paint super aplikacja")

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
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

    clock = pygame.time.Clock()

    menu_controller = MenuController(screen)

    running = True
    while running:
        running = menu_controller.process_input()
        menu_controller.update_view()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()

