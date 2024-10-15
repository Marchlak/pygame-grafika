class LineModel:
    def __init__(self):
        self.lines = []
        self.current_line = None
        self.brush_size = 3

    def start_line(self, start_pos, brush_size, color):
        self.brush_size = brush_size
        self.current_line = {
            'start_pos': start_pos,
            'end_pos': start_pos,
            'brush_size': brush_size,
            'color': color
        }

    def update_line(self, current_pos):
        if self.current_line:
            self.current_line['end_pos'] = current_pos

    def end_line(self):
        if self.current_line:
            self.lines.append(self.current_line)
        self.current_line = None

    def clear(self):
        self.lines = []
        self.current_line = None

