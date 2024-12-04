# controller/bezier_controller.py

import math
import threading

import pygame

from components.choose_file import choose_file
from components.text_input import TextInput


class BezierController:
    def __init__(self, model, view):
        self.model = model
        self.view = view
        self.exit_request = False

        self.font = pygame.font.Font(None, 24)
        self.text_inputs = []
        self.create_initial_text_input()

        self.dragging_point_index = None

        self.finish_button_rect = pygame.Rect(10, 500, 150, 30)
        self.finish_button_label = self.font.render(
            "Finish Drawing", True, (255, 255, 255)
        )

        self.add_button_rect = pygame.Rect(10, 50, 30, 30)
        self.add_button_label = self.font.render("+", True, (255, 255, 255))

        self.back_button_rect = pygame.Rect(1800, 10, 100, 30)
        self.back_button_label = self.font.render("Back", True, (255, 255, 255))


        self.create_translation_inputs()
        self.translate_button_rect = pygame.Rect(10, 550, 100, 30)
        self.translate_button_label = self.font.render(
            "Translate", True, (255, 255, 255)
        )

        self.toggle_drawing_button_rect = pygame.Rect(10, 590, 150, 30)
        self.mouse_drawing_enabled = True
        self.update_toggle_drawing_label()

        self.toggle_mode_button_rect = pygame.Rect(10, 790, 150, 30)
        self.update_toggle_mode_label()

        self.save_button_rect = pygame.Rect(10, 830, 100, 30)
        self.save_button_label = self.font.render("Save", True, (255, 255, 255))

        self.load_button_rect = pygame.Rect(120, 830, 100, 30)
        self.load_button_label = self.font.render("Load", True, (255, 255, 255))

        self.rotation_input = TextInput(
            10,
            630,
            100,
            25,
            self.font,
            placeholder="Angle (°)",
            input_type="float",
        )
        self.rotate_button_rect = pygame.Rect(10, 670, 100, 30)
        self.rotate_button_label = self.font.render("Rotate", True, (255, 255, 255))

        self.scale_input = TextInput(
            10,
            710,
            200,
            25,
            self.font,
            placeholder="Scale (%)",
            input_type="float",
            max_value=1000,
        )
        self.scale_button_rect = pygame.Rect(10, 750, 100, 30)
        self.scale_button_label = self.font.render("Scale", True, (255, 255, 255))

        self.max_x = 1920
        self.max_y = 1080

        self.moving_curve = False
        self.rotating_curve = False
        self.rotation_start_angle = 0
        self.rotation_total_angle = 0
        self.initial_rotation_total_angle = 0

        self.original_points = []
        self.update_original_points()
        self.update_buttons_positions()

    def create_initial_text_input(self):
        input_x = TextInput(
            10,
            10,
            100,
            25,
            self.font,
            text="960",
            placeholder="P0 x",
            input_type="int",
        )
        input_y = TextInput(
            120,
            10,
            100,
            25,
            self.font,
            text="540",
            placeholder="P0 y",
            input_type="int",
        )
        self.text_inputs.append((input_x, input_y))
        self.model.add_point((960, 540))

    def create_translation_inputs(self):
        x = 10
        y = 510
        self.dx_input = TextInput(
            x,
            y,
            100,
            25,
            self.font,
            placeholder="dx",
            input_type="int",
        )
        self.dy_input = TextInput(
            x + 110,
            y,
            100,
            25,
            self.font,
            placeholder="dy",
            input_type="int",
        )

    def execute_load_image(self):
        thread = threading.Thread(target=self._choose_file_thread, daemon=True)
        thread.start()

    def _choose_file_thread(self):
        file_path = choose_file()
        if file_path:
            try:
                image = pygame.image.load(file_path).convert_alpha()
                width, height = image.get_size()
                if width > 800 or height > 800:
                    self._show_error_message(
                        "Obraz jest zbyt duży. Maksymalny rozmiar to 800x800 pikseli."
                    )
                    return

                self.loaded_image = image
                self.binarised_image = None
            except pygame.error as e:
                self.view.display_message(f"Nie udało się załadować obrazu: {e}")

    def update_toggle_drawing_label(self):
        label_text = "Drawing: ON" if self.mouse_drawing_enabled else "Drawing: OFF"
        self.toggle_drawing_button_label = self.font.render(
            label_text, True, (255, 255, 255)
        )

    def process_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.exit_request = True
                return False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.exit_request = True
                    return False

            clicked_on_ui = False

            rotation_input_consumed = self.rotation_input.handle_event(event)
            if rotation_input_consumed:
                clicked_on_ui = True

            scale_input_consumed = self.scale_input.handle_event(event)
            if scale_input_consumed:
                clicked_on_ui = True

            dx_consumed = self.dx_input.handle_event(event)
            dy_consumed = self.dy_input.handle_event(event)
            if dx_consumed or dy_consumed:
                clicked_on_ui = True

            for idx, (input_x, input_y) in enumerate(self.text_inputs):
                input_x_consumed = input_x.handle_event(event)
                input_y_consumed = input_y.handle_event(event)
                if input_x_consumed or input_y_consumed:
                    clicked_on_ui = True

                x_text = input_x.get_raw_text()
                y_text = input_y.get_raw_text()
                if x_text.strip() and y_text.strip():
                    try:
                        x = int(x_text.strip())
                        y = int(y_text.strip())

                        x = max(0, min(self.max_x, x))
                        y = max(0, min(self.max_y, y))

                        if idx < len(self.model.current_control_points):
                            self.model.update_point(idx, (x, y))
                        else:
                            if len(self.model.current_control_points) < 15:
                                self.model.add_point((x, y))
                                self.update_original_points()
                    except ValueError:
                        pass
                else:
                    if idx < len(self.model.current_control_points):
                        self.model.update_point(idx, None)

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = event.pos
                if event.button == 1:
                    if (
                        self.add_button_rect.collidepoint(pos)
                        or self.finish_button_rect.collidepoint(pos)
                        or self.translate_button_rect.collidepoint(pos)
                        or self.toggle_drawing_button_rect.collidepoint(pos)
                        or self.rotate_button_rect.collidepoint(pos)
                        or self.scale_button_rect.collidepoint(pos)
                        or self.toggle_mode_button_rect.collidepoint(pos)
                        or self.save_button_rect.collidepoint(pos)
                        or self.load_button_rect.collidepoint(pos)
                        or self.back_button_rect.collidepoint(pos)
                    ):
                        clicked_on_ui = True
                        if self.add_button_rect.collidepoint(pos):
                            self.add_text_input()
                            self.update_buttons_positions()
                        elif self.finish_button_rect.collidepoint(pos):
                            self.finish_drawing()
                        elif self.translate_button_rect.collidepoint(pos):
                            self.translate_curve()
                        elif self.toggle_drawing_button_rect.collidepoint(pos):
                            self.mouse_drawing_enabled = not self.mouse_drawing_enabled
                            self.update_toggle_drawing_label()
                        elif self.rotate_button_rect.collidepoint(pos):
                            self.rotate_curve()
                        elif self.scale_button_rect.collidepoint(pos):
                            self.scale_curve()
                        elif self.toggle_mode_button_rect.collidepoint(pos):
                            self.model.toggle_drawing_mode()
                            self.update_toggle_mode_label()
                        elif self.save_button_rect.collidepoint(pos):
                            self.save_model()
                        elif self.load_button_rect.collidepoint(pos):
                            self.load_model()
                        elif self.back_button_rect.collidepoint(pos):
                            self.exit_request = True

                    else:
                        if not clicked_on_ui:
                            if self.is_over_move_handle(pos):
                                self.moving_curve = True
                                self.last_mouse_pos = pos
                            elif self.mouse_drawing_enabled:
                                index = self.get_point_at_position(pos)
                                if index is not None:
                                    self.dragging_point_index = index
                                else:
                                    if len(self.model.current_control_points) < 15:
                                        self.model.add_point(pos)
                                        self.add_text_input()
                                        idx = len(self.text_inputs) - 1
                                        input_x, input_y = self.text_inputs[idx]
                                        input_x.set_raw_text(str(pos[0]))
                                        input_y.set_raw_text(str(pos[1]))
                                        self.update_buttons_positions()
                                        self.update_original_points()
                            else:
                                pass
                elif event.button == 3:
                    if not clicked_on_ui:
                        self.rotating_curve = True
                        self.rotation_start_angle = self.calculate_angle(pos)
                        self.initial_rotation_total_angle = self.rotation_total_angle

            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    self.dragging_point_index = None
                    self.moving_curve = False
                elif event.button == 3:
                    self.rotating_curve = False

            elif event.type == pygame.MOUSEMOTION:
                if self.dragging_point_index is not None:

                    x = max(0, min(self.max_x, event.pos[0]))
                    y = max(0, min(self.max_y, event.pos[1]))

                    self.model.update_point(self.dragging_point_index, (x, y))
                    input_x, input_y = self.text_inputs[self.dragging_point_index]
                    input_x.set_raw_text(str(int(x)))
                    input_y.set_raw_text(str(int(y)))
                    self.update_original_points()
                elif self.rotating_curve:
                    current_angle = self.calculate_angle(event.pos)
                    angle_difference = current_angle - self.rotation_start_angle
                    angle_difference = (angle_difference + math.pi) % (
                        2 * math.pi
                    ) - math.pi
                    self.rotation_total_angle = (
                        self.initial_rotation_total_angle + angle_difference
                    )
                    self.apply_rotation(self.rotation_total_angle)
                elif self.moving_curve:
                    dx = event.pos[0] - self.last_mouse_pos[0]
                    dy = event.pos[1] - self.last_mouse_pos[1]
                    self.move_curve(dx, dy)
                    self.last_mouse_pos = event.pos
                elif self.view.is_hovering_nerd_image(event.pos):
                    self.view.show_tooltip = True
                else:
                    self.view.show_tooltip = False

            if event.type == pygame.MOUSEWHEEL:
                if not clicked_on_ui:
                    scale_factor = 1 + (event.y * 0.1)
                    self.scale_curve_by_factor(scale_factor)

        return True

    def scale_curve(self):
        scale_text = self.scale_input.get_raw_text()
        if scale_text.strip():
            try:
                scale_percentage = float(scale_text.strip())
                scale_factor = scale_percentage / 100.0
                self.apply_scale(scale_factor)
                self.scale_input.set_raw_text("")
            except ValueError:
                pass

    def scale_curve_by_factor(self, scale_factor):
        self.apply_scale(scale_factor)
        self.update_original_points()

    def apply_scale(self, scale_factor):
        centroid = self.get_centroid(self.original_points)
        for idx, original_point in enumerate(self.model.current_control_points):
            if original_point is not None:
                x = original_point[0] - centroid[0]
                y = original_point[1] - centroid[1]
                x_new = x * scale_factor
                y_new = y * scale_factor
                x_final = x_new + centroid[0]
                y_final = y_new + centroid[1]
                self.model.update_point(idx, (x_final, y_final))
                input_x, input_y = self.text_inputs[idx]
                input_x.set_raw_text(str(int(x_final)))
                input_y.set_raw_text(str(int(y_final)))
        self.update_original_points()

    def get_point_at_position(self, pos):
        for i, point in enumerate(self.model.get_current_points()):
            if point is not None:
                dx = pos[0] - point[0]
                dy = pos[1] - point[1]
                distance_squared = dx * dx + dy * dy
                if distance_squared <= self.view.control_point_radius**2:
                    return i
        return None

    def is_over_move_handle(self, pos):
        move_handle_pos = self.get_centroid(self.original_points)
        dx = pos[0] - move_handle_pos[0]
        dy = pos[1] - move_handle_pos[1]
        distance_squared = dx * dx + dy * dy
        return distance_squared <= self.view.move_handle_radius**2

    def finish_drawing(self):
        self.model.finish_current_curve()
        self.text_inputs.clear()
        self.create_initial_text_input()
        self.update_buttons_positions()
        self.update_original_points()

    def add_text_input(self):
        idx = len(self.text_inputs)
        if idx >= 15:
            return

        x = 10
        y = 10 + idx * 30
        input_x = TextInput(
            x,
            y,
            100,
            25,
            self.font,
            placeholder=f"P{idx} x",
            input_type="int",
        )
        input_y = TextInput(
            x + 110,
            y,
            100,
            25,
            self.font,
            placeholder=f"P{idx} y",
            input_type="int",
        )
        self.text_inputs.append((input_x, input_y))
        self.update_buttons_positions()

    def update_buttons_positions(self):
        last_idx = len(self.text_inputs) - 1
        x = 10
        y = 10 + (last_idx + 1) * 30
        self.add_button_rect.topleft = (x, y)
        self.finish_button_rect.topleft = (x + 50, y)
        self.dx_input.rect.topleft = (x, y + 50)
        self.dy_input.rect.topleft = (x + 110, y + 50)
        self.translate_button_rect.topleft = (x, y + 90)
        self.toggle_drawing_button_rect.topleft = (x, y + 130)
        self.rotation_input.rect.topleft = (x, y + 170)
        self.rotate_button_rect.topleft = (x, y + 210)
        self.scale_input.rect.topleft = (x, y + 250)
        self.scale_button_rect.topleft = (x, y + 290)
        self.toggle_mode_button_rect.topleft = (x, y + 330)
        self.save_button_rect.topleft = (x, y + 370)
        self.load_button_rect.topleft = (x + 110, y + 370)

    def translate_curve(self):
        dx_text = self.dx_input.get_raw_text()
        dy_text = self.dy_input.get_raw_text()
        if dx_text.strip() and dy_text.strip():
            try:
                dx = int(dx_text.strip())
                dy = int(dy_text.strip())
                self.move_curve(dx, dy)
                self.dx_input.set_raw_text("")
                self.dy_input.set_raw_text("")
            except ValueError:
                pass

    def move_curve(self, dx, dy):
        for idx, point in enumerate(self.model.current_control_points):
            if point is not None:
                new_x = max(0, min(self.max_x, point[0] + dx))
                new_y = max(0, min(self.max_y, point[1] + dy))
                self.model.update_point(idx, (new_x, new_y))
                input_x, input_y = self.text_inputs[idx]
                input_x.set_raw_text(str(int(new_x)))
                input_y.set_raw_text(str(int(new_y)))
        self.update_original_points()

    def rotate_curve(self):
        angle_text = self.rotation_input.get_raw_text()
        if angle_text.strip():
            try:
                angle_degrees = float(angle_text.strip())
                angle_radians = math.radians(angle_degrees)
                self.rotation_total_angle += angle_radians
                self.apply_rotation(self.rotation_total_angle)
                self.rotation_input.set_raw_text("")
            except ValueError:
                pass

    def apply_rotation(self, angle_radians):
        centroid = self.get_centroid(self.original_points)
        sin_angle = math.sin(angle_radians)
        cos_angle = math.cos(angle_radians)
        for idx, original_point in enumerate(self.original_points):
            if original_point is not None:
                x = original_point[0] - centroid[0]
                y = original_point[1] - centroid[1]
                x_new = x * cos_angle - y * sin_angle
                y_new = x * sin_angle + y * cos_angle
                x_final = x_new + centroid[0]
                y_final = y_new + centroid[1]
                self.model.update_point(idx, (x_final, y_final))
                input_x, input_y = self.text_inputs[idx]
                input_x.set_raw_text(str(int(x_final)))
                input_y.set_raw_text(str(int(y_final)))

    def calculate_angle(self, pos):
        centroid = self.get_centroid(self.original_points)
        dx = pos[0] - centroid[0]
        dy = pos[1] - centroid[1]
        return math.atan2(dy, dx)

    def get_centroid(self, points):
        valid_points = [p for p in points if p is not None]
        if valid_points:
            x_sum = sum(point[0] for point in valid_points)
            y_sum = sum(point[1] for point in valid_points)
            n = len(valid_points)
            return (x_sum / n, y_sum / n)
        else:
            return (0, 0)

    def update_original_points(self):
        self.original_points = [p for p in self.model.current_control_points]
        self.rotation_total_angle = 0

    def update_view(self):
        self.view.screen.fill((255, 255, 255))

        current_points = [
            pt for pt in self.model.get_current_points() if pt is not None
        ]

        move_handle_pos = self.get_centroid(current_points) if current_points else None

        self.view.draw(
            self.model.get_all_curves(),
            current_points,
            move_handle_pos,
            self.model.get_drawing_mode(),
        )

        for input_x, input_y in self.text_inputs:
            input_x.draw(self.view.screen)
            input_y.draw(self.view.screen)

        pygame.draw.rect(self.view.screen, (0, 200, 0), self.add_button_rect)
        self.view.screen.blit(
            self.add_button_label,
            (self.add_button_rect.x + 5, self.add_button_rect.y + 5),
        )

        pygame.draw.rect(self.view.screen, (0, 0, 255), self.finish_button_rect)
        self.view.screen.blit(
            self.finish_button_label,
            (self.finish_button_rect.x + 5, self.finish_button_rect.y + 5),
        )

        self.dx_input.draw(self.view.screen)
        self.dy_input.draw(self.view.screen)
        pygame.draw.rect(self.view.screen, (0, 0, 255), self.translate_button_rect)
        self.view.screen.blit(
            self.translate_button_label,
            (self.translate_button_rect.x + 5, self.translate_button_rect.y + 5),
        )

        pygame.draw.rect(
            self.view.screen, (128, 0, 128), self.toggle_drawing_button_rect
        )
        self.view.screen.blit(
            self.toggle_drawing_button_label,
            (
                self.toggle_drawing_button_rect.x + 5,
                self.toggle_drawing_button_rect.y + 5,
            ),
        )

        self.rotation_input.draw(self.view.screen)
        pygame.draw.rect(self.view.screen, (0, 0, 255), self.rotate_button_rect)
        self.view.screen.blit(
            self.rotate_button_label,
            (self.rotate_button_rect.x + 5, self.rotate_button_rect.y + 5),
        )

        self.scale_input.draw(self.view.screen)
        pygame.draw.rect(self.view.screen, (0, 0, 255), self.scale_button_rect)
        self.view.screen.blit(
            self.scale_button_label,
            (self.scale_button_rect.x + 5, self.scale_button_rect.y + 5),
        )

        pygame.draw.rect(self.view.screen, (255, 165, 0), self.toggle_mode_button_rect)
        self.view.screen.blit(
            self.toggle_mode_button_label,
            (self.toggle_mode_button_rect.x + 5, self.toggle_mode_button_rect.y + 5),
        )

        pygame.draw.rect(self.view.screen, (0, 128, 0), self.save_button_rect)

        self.view.screen.blit(
            self.back_button_label,
            (self.back_button_rect.x + 5, self.back_button_rect.y + 5),
        )
        pygame.draw.rect(self.view.screen, (255, 0, 0), self.back_button_rect)
        self.view.screen.blit(
            self.back_button_label,
            (self.back_button_rect.x + 5, self.back_button_rect.y + 5),
        )

        self.view.screen.blit(
            self.save_button_label,
            (self.save_button_rect.x + 5, self.save_button_rect.y + 5),
        )
        pygame.draw.rect(self.view.screen, (0, 128, 0), self.load_button_rect)
        self.view.screen.blit(
            self.load_button_label,
            (self.load_button_rect.x + 5, self.load_button_rect.y + 5),
        )

        pygame.display.flip()

    def update_toggle_mode_label(self):
        mode = self.model.get_drawing_mode()
        label_text = f"Mode: {mode.capitalize()}"
        self.toggle_mode_button_label = self.font.render(
            label_text, True, (255, 255, 255)
        )

    def save_model(self):
        file_name = "bezier_model.pkl"
        self.model.save_model(file_name)
        self.view.display_message("Model saved.")

    def load_model(self):
        thread = threading.Thread(target=self._choose_file_thread, daemon=True)
        thread.start()

    def _choose_file_thread(self):
        file_path = choose_file()
        if file_path:
            try:
                self.model.load_model(file_path)

                self.update_text_inputs_after_load()
                self.view.display_message("Model załadowany.")
            except Exception as e:
                self._show_error_message(f"Nie udało się załadować modelu: {e}")
        else:
            self.view.display_message("Nie wybrano żadnego pliku.")

    def update_text_inputs_after_load(self):
        self.text_inputs.clear()
        for idx, point in enumerate(self.model.current_control_points):
            if point is not None:
                x = point[0]
                y = point[1]
                input_x = TextInput(
                    10,
                    10 + idx * 30,
                    100,
                    25,
                    self.font,
                    text=str(int(x)),
                    placeholder=f"P{idx} x",
                    input_type="int",
                )
                input_y = TextInput(
                    120,
                    10 + idx * 30,
                    100,
                    25,
                    self.font,
                    text=str(int(y)),
                    placeholder=f"P{idx} y",
                    input_type="int",
                )
                self.text_inputs.append((input_x, input_y))
        self.update_buttons_positions()
