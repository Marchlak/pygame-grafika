from interfaces import IController
import pygame

class ColorConversionController(IController):
    def __init__(self, model, view):
        self.model = model
        self.view = view
        self.exit_request = False

    def process_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.exit_request = True
            else:
                self.view.handle_event(event)

        rr = self.view.slider_r.value
        gg, bb = self.view.color_area.get_values()


        r,g,b  = self.view.get_rgb_values()
        c,m,y,k = self.view.get_cmyk_values()
        h,s,v = self.view.get_hsv_values()


        if (rr, gg, bb) != self.model.rgb:
            self.model.set_rgb(rr, gg, bb)
            self.view.set_hsv_values(self.model.hsv)
            self.view.set_cmyk_values(self.model.cmyk)
            self.view.set_rgb_values(self.model.rgb)
            self.view.slider_r.set_value(self.model.rgb[0])
            self.view.color_area.set_selected_pos_based_on_gb(self.model.rgb[1], self.model.rgb[2])

        elif (r, g, b) != self.model.rgb:
            self.model.set_rgb(r, g, b)
            self.view.set_hsv_values(self.model.hsv)
            self.view.set_cmyk_values(self.model.cmyk)
            self.view.set_rgb_values(self.model.rgb)
            self.view.slider_r.set_value(self.model.rgb[0])
            self.view.color_area.set_selected_pos_based_on_gb(self.model.rgb[1], self.model.rgb[2])

        elif (h, s, v) != self.model.hsv:
            self.model.set_hsv(h, s, v)
            self.view.set_hsv_values(self.model.hsv)
            self.view.set_cmyk_values(self.model.cmyk)
            self.view.set_rgb_values(self.model.rgb)
            self.view.slider_r.set_value(self.model.rgb[0])
            self.view.color_area.set_selected_pos_based_on_gb(self.model.rgb[1], self.model.rgb[2])

        elif (c, m, y, k) != self.model.cmyk:
            self.model.set_cmyk(c, m, y, k)
            self.view.set_hsv_values(self.model.hsv)
            self.view.set_cmyk_values(self.model.cmyk)
            self.view.set_rgb_values(self.model.rgb)
            self.view.slider_r.set_value(self.model.rgb[0])
            self.view.color_area.set_selected_pos_based_on_gb(self.model.rgb[1], self.model.rgb[2])


        self.view.draw({
            'rgb': self.model.rgb,
            'cmyk': self.model.cmyk,
            'hsv': self.model.hsv
        })

        self.exit_request = self.view.exit_request

        pygame.time.Clock().tick(60)
        return True

    def check_button_click(self, pos):
        for button in self.view.buttons:
            if button["rect"].collidepoint(pos):
                if "action" in button and button["action"] == "back_to_menu":
                    self.exit_request = True

    def update_view(self):
        pass

