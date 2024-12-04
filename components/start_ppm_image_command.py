from components.command import Command

class StartPPMImageCommand(Command):
    def __init__(self, menu_controller):
        self.menu_controller = menu_controller

    def execute(self):
        self.menu_controller.start_ppm_image_controller()

