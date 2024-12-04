import pygame
from components.text_input import TextInput

class KernelInputGrid:
    def __init__(self, x, y, cell_size, font, kernel_size=3, min_value=-100, max_value=100):
        self.x = x 
        self.y = y
        self.cell_size = cell_size
        self.font = font
        self.kernel_size = kernel_size
        self.min_value = min_value
        self.max_value = max_value
        self.inputs = []
        self.create_grid()

    def create_grid(self):
        self.inputs = []
        for row in range(self.kernel_size):
            input_row = []
            for col in range(self.kernel_size):
                input_box = TextInput(
                    x=self.x + col * self.cell_size,
                    y=self.y + row * self.cell_size,
                    width=self.cell_size,
                    height=self.cell_size,
                    font=self.font,
                    text='0',
                    placeholder='0',
                    max_length=5,
                    input_type='float',
                    min_value=self.min_value,
                    max_value=self.max_value
                )
                input_row.append(input_box)
            self.inputs.append(input_row)

    def handle_event(self, event):
        for row in self.inputs:
            for input_box in row:
                input_box.handle_event(event)

    def update(self):
        for row in self.inputs:
            for input_box in row:
                input_box.update()

    def draw(self, screen):
        for row in self.inputs:
            for input_box in row:
                input_box.draw(screen)

    def get_kernel_values(self):
        values = []
        for row in self.inputs:
            value_row = []
            for input_box in row:
                value = float(input_box.get_text())
                value_row.append(value)
            values.append(value_row)
        return values

    def set_kernel_size(self, new_size):
        if 2 <= new_size <= 9:
            self.kernel_size = new_size
            self.create_grid()
        else:
            print("Kernel size must be between 2 and 9.")

