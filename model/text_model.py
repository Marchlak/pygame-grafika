class TextModel:
    def __init__(self):
        self.texts = []
        self.current_text = None
        self.selected_text = None

    def start_text(self, start_pos, color, font_size):
        self.current_text = {
            'start_pos': start_pos,
            'text': '',
            'color': color,
            'font_size': font_size
        }

    def update_text(self, new_char):
        if self.current_text:
            self.current_text['text'] += new_char

    def end_text(self):
        if self.current_text:
            self.texts.append(self.current_text)
            self.selected_text = self.current_text
            self.current_text = None

    def clear(self):
        self.texts = []
        self.current_text = None
        self.selected_text = None
