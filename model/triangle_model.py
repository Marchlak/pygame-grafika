class TriangleModel:
    def __init__(self):
        self.triangles = []
        self.current_triangle = None
        self.selected_triangle = None


    def start_triangle(self, start_pos):
        self.current_triangle = {
            'start_pos': start_pos,
            'width': 0,
            'height': 0,
            'angle': 0,
            'scale': 1
        }

    def update_triangle(self, current_pos):
        if self.current_triangle:
            start_pos = self.current_triangle['start_pos']
            self.current_triangle['width'] = current_pos[0] - start_pos[0]
            self.current_triangle['height'] = current_pos[1] - start_pos[1]

    def end_triangle(self):
        if self.current_triangle:
            self.triangles.append(self.current_triangle)
            self.selected_triangle = self.current_triangle
        self.current_triangle = None

    def move(self, dx, dy):
        if self.selected_triangle:
            start_pos = self.selected_triangle['start_pos']
            self.selected_triangle['start_pos'] = (start_pos[0] + dx, start_pos[1] + dy)

    def rotate(self, angle):
        if self.selected_triangle:
            self.selected_triangle['angle'] += angle

    def scale(self, scale_factor):
        if self.selected_triangle:
            self.selected_triangle['scale'] *= scale_factor

    def clear(self):
        self.triangles = []
        self.current_triangle = None
        self.selected_triangle = None

