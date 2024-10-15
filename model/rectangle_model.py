class RectangleModel:
    def __init__(self):
        self.rectangles = []
        self.current_rectangle = None
        self.selected_rectangle = None

    def start_rectangle(self, start_pos):
        self.current_rectangle = {'start_pos': start_pos, 'width': 0, 'height': 0, 'angle': 0, 'scale': 1}

    def update_rectangle(self, current_pos):
        if self.current_rectangle:
            start_pos = self.current_rectangle['start_pos']
            self.current_rectangle['width'] = current_pos[0] - start_pos[0]
            self.current_rectangle['height'] = current_pos[1] - start_pos[1]

    def end_rectangle(self):
        if self.current_rectangle:
            self.rectangles.append(self.current_rectangle)
            self.selected_rectangle = self.current_rectangle
        self.current_rectangle = None

    def move(self, dx, dy):
        if self.selected_rectangle:
            start_pos = self.selected_rectangle['start_pos']
            self.selected_rectangle['start_pos'] = (start_pos[0] + dx, start_pos[1] + dy)

    def rotate(self, angle):
        if self.selected_rectangle:
            self.selected_rectangle['angle'] += angle

    def scale(self, scale_factor):
        if self.selected_rectangle:
            self.selected_rectangle['scale'] *= scale_factor

    def clear(self):
        self.rectangles = []
        self.current_rectangle = None
        self.selected_rectangle = None

