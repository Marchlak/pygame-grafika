# model/bezier_model.py

import os
import pickle

class BezierModel:
    def __init__(self):
        self.curves = []
        self.current_control_points = []
        self.drawing_mode = 'bezier' 

    def add_point(self, point):
        self.current_control_points.append(point)

    def update_point(self, index, point):
        if 0 <= index < len(self.current_control_points):
            self.current_control_points[index] = point

    def get_current_points(self):
        return self.current_control_points

    def set_current_points(self, points):
        self.current_control_points = points

    def clear_current_points(self):
        self.current_control_points = []

    def finish_current_curve(self):
        valid_points = [pt for pt in self.current_control_points if pt is not None]
        if valid_points:
            self.curves.append({
                'points': valid_points,
                'mode': self.drawing_mode,
            })
        self.clear_current_points()

    def get_all_curves(self):
        return self.curves

    def toggle_drawing_mode(self):
        self.drawing_mode = 'polygon' if self.drawing_mode == 'bezier' else 'bezier'

    def get_drawing_mode(self):
        return self.drawing_mode


    def save_model(self, file_name):
        save_dir = os.path.join(os.getcwd(), 'save_bezier')
        os.makedirs(save_dir, exist_ok=True)

        file_path = os.path.join(save_dir, file_name)

        data = {
            'curves': self.curves,
            'current_control_points': self.current_control_points,
            'drawing_mode': self.drawing_mode,
        }

        try:
            with open(file_path, 'wb') as f:
                pickle.dump(data, f)
            print(f"Model saved to {file_path}")
        except Exception as e:
            print(f"Error saving model: {e}")

    def load_model(self, file_name):
        save_dir = os.path.join(os.getcwd(), 'save_bezier')
        file_path = os.path.join(save_dir, file_name)

        try:
            with open(file_path, 'rb') as f:
                data = pickle.load(f)
            self.curves = data.get('curves', [])
            self.current_control_points = data.get('current_control_points', [])
            self.drawing_mode = data.get('drawing_mode', 'bezier')
            print(f"Model loaded from {file_path}")
        except Exception as e:
            print(f"Error loading model: {e}")

