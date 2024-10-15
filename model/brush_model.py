class BrushModel:
    def __init__(self):
        self.lines = []
        self.current_line = []
        self.brush_size = 3

    def add_point(self, point):
        self.current_line.append(point)

    def end_line(self):
        if self.current_line:
            self.lines.append((self.current_line, self.brush_size))
        self.current_line = []

    def set_brush_size(self, size):
        self.brush_size = size

    def clear(self):
        self.current_line = []
        self.lines = []

