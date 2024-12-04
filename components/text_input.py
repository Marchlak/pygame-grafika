import pygame

class TextInput:
    def __init__(
        self, 
        x, y, width, height, font, 
        text='', placeholder='', 
        max_length=10, 
        color_inactive=(200, 200, 200), 
        color_active=(255, 255, 255), 
        text_color=(0, 0, 0),
        input_type='int',
        min_value=0,
        max_value=100
    ):
        self.rect = pygame.Rect(x, y, width, height)
        self.color_inactive = color_inactive
        self.color_active = color_active
        self.text_color = text_color
        self.color = self.color_inactive
        self.font = font
        self.text = text
        self.placeholder = placeholder
        self.input_type = input_type
        self.min_value = min_value
        self.max_value = max_value
        self.active = False
        self.max_length = max_length

        self.confirmed_text = self.text if self.text else self.placeholder
        self.update_text_surface()

    def update_text_surface(self):
        display_text = self.text if self.text else self.placeholder
        self.txt_surface = self.font.render(display_text, True, self.text_color if self.text else (150, 150, 150))

    def handle_event(self, event):
        event_consumed = False
        if event.type == pygame.MOUSEBUTTONDOWN:

            if self.rect.collidepoint(event.pos):
                self.active = True
                self.color = self.color_active
                event_consumed = True  # The event was consumed
            else:
                if self.active:
                    self.format_text()
                self.active = False
                self.color = self.color_inactive

        if self.active:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    self.active = False
                    self.color = self.color_inactive
                    self.format_text()
                elif event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    if self.input_type == 'int':
                        if (event.unicode.isdigit() or
                            (event.unicode == '-' and self.text == '')):
                            if len(self.text) < self.max_length:
                                self.text += event.unicode
                    elif self.input_type == 'float':
                        if (event.unicode.isdigit() or
                            (event.unicode == '.' and '.' not in self.text) or
                            (event.unicode == '-' and self.text == '')):
                            if len(self.text) < self.max_length:
                                self.text += event.unicode
                self.update_text_surface()
                event_consumed = True

        return event_consumed  

    def format_text(self):
        if self.input_type == 'int':
            if self.text in ('-', ''):
                value = self.min_value
            else:
                try:
                    value = int(self.text)
                except ValueError:
                    value = self.min_value
            value = max(self.min_value, min(self.max_value, value))
            self.confirmed_text = str(value)
            self.text = self.confirmed_text
        elif self.input_type == 'float':
            if self.text in ('-', '.', '-.', ''):
                value = self.min_value
            else:
                try:
                    value = float(self.text)
                except ValueError:
                    value = self.min_value
            value = max(self.min_value, min(self.max_value, value))
            self.confirmed_text = f"{value:.2f}"
            self.text = self.confirmed_text
        self.update_text_surface()

    def update(self):
        width = max(200, self.txt_surface.get_width()+10)
        self.rect.w = width

    def draw(self, screen):
        screen.blit(self.txt_surface, (self.rect.x+5, self.rect.y+5))
        pygame.draw.rect(screen, self.color, self.rect, 2)

    def get_text(self):
        return self.confirmed_text if self.confirmed_text else (str(self.min_value) if self.input_type == 'int' else f"{self.min_value:.2f}")


    def set_text(self, new_text):
        if not self.active:
            if self.input_type == 'int':
                try:
                    value = int(new_text)
                except ValueError:
                    value = self.min_value
                value = max(self.min_value, min(self.max_value, value))
                self.text = str(value)
                self.confirmed_text = self.text
            elif self.input_type == 'float':
                try:
                    value = float(new_text)
                except ValueError:
                    value = self.min_value
                value = max(self.min_value, min(self.max_value, value))
                self.text = f"{value:.2f}"
                self.confirmed_text = self.text
            self.update_text_surface()


    def get_raw_text(self):
        """Returns the current text without any formatting."""
        return self.text

    def set_raw_text(self, new_text):
        """Sets the text without formatting or validation."""
        self.text = new_text
        self.update_text_surface()
