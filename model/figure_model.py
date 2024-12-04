# figure_model.py
class FigureModel:
    def __init__(self):
        self.rotation_speed = [0.001, 0.001, 0.001]

    def set_rotation_speed(self, speed):
        self.rotation_speed = speed
