from model.brush_model import BrushModel
from model.rectangle_model import RectangleModel
from model.triangle_model import TriangleModel
from model.ellipse_model import EllipseModel
from model.text_model import TextModel
from model.line_model import LineModel

class PaintModel:
    def __init__(self):
        self.brush_model = BrushModel()
        self.rectangle_model = RectangleModel()
        self.triangle_model = TriangleModel()
        self.ellipse_model = EllipseModel()
        self.text_model = TextModel()
        self.line_model = LineModel()
        self.drawing_mode = 'brush'
        self.objects = []
        self.selected_color = (0,0,0)

    def set_mode(self, mode):
        self.drawing_mode = mode

    def set_color(self, color):
        self.selected_color = color

    def add_line(self, line_points, brush_size):
        self.objects.append({
            'type': 'line',
            'points': line_points,
            'brush_size': brush_size,
            'color': self.selected_color
        })

    def add_rectangle(self, rectangle):
        self.objects.append({
            'type': 'rectangle',
            'rectangle': rectangle,
            'color': self.selected_color
        })

    def add_triangle(self, triangle):
        self.objects.append({
            'type': 'triangle',
            'triangle': triangle,
            'color': self.selected_color
        })

    def add_ellipse(self, ellipse):
        self.objects.append({
            'type': 'ellipse',
            'ellipse': ellipse,
            'color': self.selected_color
        })

    def add_text(self, text, font_size):
        self.objects.append({
            'type': 'text',
            'text': text,
            'color': self.selected_color,
            'font_size': font_size,
        })

    def add_straight_line(self, line, brush_size):
        self.objects.append({
            'type': 'sline',
            'sline': line,
            'brush_size': brush_size,
            'color': self.selected_color
        })



    def clear(self):
        self.objects = []
        self.brush_model.clear()
        self.rectangle_model.clear()
        self.triangle_model.clear()
        self.text_model.clear()
        self.line_model.clear()
        self.text_model.clear()

