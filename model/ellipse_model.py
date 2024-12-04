class EllipseModel:
    def __init__(self):
        self.ellipses = []
        self.current_ellipse = None
        self.selected_ellipse = None

    def start_ellipse(self, start_pos):
        """Rozpocznij rysowanie elipsy."""
        self.current_ellipse = {
            'start_pos': start_pos,
            'width': 0,
            'height': 0,
            'angle': 0,
            'scale': 1
        }

    def update_ellipse(self, current_pos):
        """Aktualizuj wymiary bieżącej elipsy."""
        if self.current_ellipse:
            start_pos = self.current_ellipse['start_pos']
            self.current_ellipse['width'] = current_pos[0] - start_pos[0]
            self.current_ellipse['height'] = current_pos[1] - start_pos[1]

    def end_ellipse(self):
        """Zakończ rysowanie elipsy."""
        if self.current_ellipse:
            self.ellipses.append(self.current_ellipse)
            self.selected_ellipse = self.current_ellipse
        self.current_ellipse = None

    def move(self, dx, dy):
        """Przesuń wybraną elipsę."""
        if self.selected_ellipse:
            start_pos = self.selected_ellipse['start_pos']
            self.selected_ellipse['start_pos'] = (start_pos[0] + dx, start_pos[1] + dy)

    def rotate(self, angle):
        """Obróć wybraną elipsę."""
        if self.selected_ellipse:
            self.selected_ellipse['angle'] += angle

    def scale(self, scale_factor):
        """Skaluj wybraną elipsę."""
        if self.selected_ellipse:
            self.selected_ellipse['scale'] *= scale_factor

    def clear(self):
        """Wyczyść wszystkie narysowane elipsy."""
        self.ellipses = []
