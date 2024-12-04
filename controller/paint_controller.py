import pygame
import os

class PaintController:
    def __init__(self, model, view):
        self.model = model
        self.view = view
        self.drawing = False
        self.typing = True
        self.current_color = (0, 0, 0)
        self.font_size = 24
        self.exit_request = False

    def process_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    self.drawing = True

                    if self.view.is_color_palette_click(event.pos):
                        selected_color = self.view.get_color_from_palette(event.pos)
                        self.model.set_color(selected_color)
                        self.current_color = selected_color
                    elif self.is_button_click(event.pos):
                        self.check_button_click(event.pos)
                    elif self.model.drawing_mode == 'brush':
                        self.model.brush_model.add_point(event.pos)
                    elif self.model.drawing_mode == 'rectangle':
                        self.model.rectangle_model.start_rectangle(event.pos)
                    elif self.model.drawing_mode == 'triangle':
                        self.model.triangle_model.start_triangle(event.pos)
                    elif self.model.drawing_mode == 'ellipse':
                        self.model.ellipse_model.start_ellipse(event.pos)
                    elif self.model.drawing_mode == 'ellipse':
                        self.model.add_ellipse(self.model.ellipse_model.current_ellipse)
                        self.model.ellipse_model.start_ellipse()
                    elif self.model.drawing_mode == 'line':
                        self.model.line_model.start_line(event.pos, self.model.brush_model.brush_size, self.current_color)
                    elif self.model.drawing_mode == 'text':
                        if self.model.text_model.current_text:
                            self.model.add_text(self.model.text_model.current_text, self.font_size)
                            self.model.text_model.end_text()
                        self.model.text_model.start_text(event.pos, self.current_color, self.font_size)

            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    self.drawing = False
                    if self.model.drawing_mode == 'brush':
                        self.model.add_line(self.model.brush_model.current_line, self.model.brush_model.brush_size)
                        self.model.brush_model.end_line()
                    elif self.model.drawing_mode == 'rectangle':
                        self.model.add_rectangle(self.model.rectangle_model.current_rectangle)
                        self.model.rectangle_model.end_rectangle()
                    elif self.model.drawing_mode == 'triangle':
                        self.model.add_triangle(self.model.triangle_model.current_triangle)
                        self.model.triangle_model.end_triangle()
                    elif self.model.drawing_mode == 'ellipse':
                        self.model.add_ellipse(self.model.ellipse_model.current_ellipse)
                        self.model.ellipse_model.end_ellipse()
                    elif self.model.drawing_mode == 'line':
                        self.model.add_straight_line(self.model.line_model.current_line, self.model.line_model.brush_size)
                        self.model.line_model.end_line()

            if event.type == pygame.MOUSEMOTION and self.drawing:
                if self.model.drawing_mode == 'brush':
                    self.model.brush_model.add_point(event.pos)
                elif self.model.drawing_mode == 'rectangle':
                    self.model.rectangle_model.update_rectangle(event.pos)
                elif self.model.drawing_mode == 'triangle':
                    self.model.triangle_model.update_triangle(event.pos)
                elif self.model.drawing_mode == 'ellipse':
                    self.model.ellipse_model.update_ellipse(event.pos)
                elif self.model.drawing_mode == 'line':
                    self.model.line_model.update_line(event.pos)

            if event.type == pygame.MOUSEMOTION:
                if self.view.is_hovering_nerd_image(event.pos):
                    self.view.show_tooltip = True
                else:
                    self.view.show_tooltip = False

            if event.type == pygame.KEYDOWN:
                if self.typing:
                    if event.key == pygame.K_BACKSPACE:
                        if len(self.model.text_model.current_text['text']) > 0:
                            self.model.text_model.current_text['text'] = self.model.text_model.current_text['text'][:-1]
                    else:
                        self.model.text_model.update_text(event.unicode)


            if(self.model.drawing_mode == 'rectangle'):
                self.move(self.model.rectangle_model)
            elif(self.model.drawing_mode == 'triangle'):
                self.move(self.model.triangle_model)
            elif self.model.drawing_mode == 'ellipse':
                self.move(self.model.ellipse_model)


        return True

    def move(self, model):
            keys = pygame.key.get_pressed()
            if keys[pygame.K_j]:
                model.move(-5, 0)
            if keys[pygame.K_l]:
                model.move(5, 0)
            if keys[pygame.K_i]:
                model.move(0, -5)
            if keys[pygame.K_k]:
                model.move(0, 5)
            if keys[pygame.K_r]:
                model.rotate(5)
            if keys[pygame.K_s]:
                model.scale(1.01)
            if keys[pygame.K_a]:
                model.scale(0.99)


    def check_button_click(self, pos):
        for button in self.view.buttons:
            if button["rect"].collidepoint(pos):
                if "size" in button:
                    self.model.brush_model.set_brush_size(button["size"])
                    if button["size"] == 3:
                        self.font_size = 24
                    elif button["size"] == 6:
                        self.font_size = 36
                    elif button["size"] == 9:
                        self.font_size = 48
                if "mode" in button:
                    self.model.drawing_mode = button["mode"]
                if "action" in button and button["action"] == "clear":
                    self.model.clear()
                if "action" in button and button["action"] == "save":
                    self.save_image()
                if "action" in button and button["action"] == "back_to_menu":
                    self.back_to_menu()

    def is_button_click(self, pos):
        for button in self.view.buttons:
            if button["rect"].collidepoint(pos) or pygame.Rect(1500, 10, 240, 40).collidepoint(pos):
                return True
        return False

    def save_image(self):
        base_filename = "save_images/my_drawing.png"
        filename = self.get_available_filename(base_filename)

        buttons_height = 52
        width = self.view.screen.get_width()
        height = self.view.screen.get_height()

        drawing_area = pygame.Surface((width, height - buttons_height))

        drawing_area.blit(self.view.screen, (0, 0), (0, buttons_height, width, height - buttons_height))

        pygame.image.save(drawing_area, filename)
        print(f"zapisano obraz jako {filename}")


    def get_available_filename(self,base_filename):
        if not os.path.exists(base_filename):
            return base_filename

        base_name, extension = os.path.splitext(base_filename)
        counter = 1
        new_filename = f"{base_name}({counter}){extension}"

        while os.path.exists(new_filename):
            counter += 1
            new_filename = f"{base_name}({counter}){extension}"

        return new_filename

    def back_to_menu(self):
        self.exit_request = True


    def update_view(self):
        self.view.render(self.model.objects, self.model.brush_model.current_line, self.model.line_model.current_line, self.model.rectangle_model.current_rectangle,
                         self.model.triangle_model.current_triangle, self.model.ellipse_model.current_ellipse,
                         self.model.text_model.current_text, self.model.brush_model.brush_size, self.current_color,
                         self.font_size, self.model.drawing_mode)
