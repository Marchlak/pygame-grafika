import os
import pygame
import time

from components.load_image_command import LoadImageCommand
from components.save_image_command import SaveImageCommand  # Zakładam, że zapisałeś SaveImageCommand w tym module

class ImageController:
    def __init__(self, model, view):
        self.model = model
        self.view = view
        self.exit_request = False
        self.load_image_command = LoadImageCommand(model)
        self.save_image_command = SaveImageCommand()
    
    def process_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.exit_request = True
                return False

            if event.type == pygame.MOUSEMOTION:
                if self.view.is_hovering_nerd_image(event.pos):
                    self.view.show_tooltip = True
                else:
                    self.view.show_tooltip = False


            if event.type == pygame.MOUSEBUTTONDOWN:
                action = self.view.get_button_action(event.pos)
                if action == "load_image":
                    self.load_image_command.execute()
                elif action == "save_image":
                    self.save_image()
                elif action == "back_to_menu":
                    self.exit_request = True

        return True

    def update_view(self):

        status, message = self.save_image_command.check_status()
        if status:
            self.view.set_message(message)


        self.load_image_command.check_process()

        if self.model.image_ready.is_set():
            self.view.update_image(self.model)
            if self.model.loading_time is not None:
                self.view.set_loading_time(self.model.loading_time) 
            self.model.image_ready.clear()
        self.view.draw()

    def save_image(self):
        if self.model.pixels.size == 0:
            print("Brak wczytanego obrazu do zapisania.")
            self.view.set_message("Brak wczytanego obrazu do zapisania.")
            return
        self.save_image_command.execute(self.model)

