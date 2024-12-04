from interfaces import IModel
import colorsys

class ColorModel(IModel):
    def __init__(self):
        self.rgb = (0, 0, 0)    # Default color
        self.cmyk = (0.0, 0.0, 0.0, 100.0)
        self.hsv = (0, 0, 0)

    def set_rgb(self, r, g, b):
        self.rgb = (r, g, b)
        self._update_cmyk_from_rgb(r, g, b)
        self._update_hsv_from_rgb(r, g, b)

    def set_cmyk(self, c, m, y, k):
        self.cmyk = (c, m, y, k)
        r, g, b = self._update_rgb_from_cmyk(c, m, y, k)
        self.rgb = (r, g, b)
        self._update_hsv_from_rgb(r, g, b)

    def set_hsv(self, h, s, v):
        self.hsv = (h, s, v)
        r, g, b = colorsys.hsv_to_rgb(h/360, s/100, v/100)
        self.rgb = (int(r * 255), int(g * 255), int(b * 255))
        self._update_cmyk_from_rgb(*self.rgb)

    def _update_cmyk_from_rgb(self, r, g, b):
        if (r, g, b) == (0, 0, 0):
            self.cmyk = (0, 0, 0, 100)
            return
        c = 1 - r / 255
        m = 1 - g / 255
        y = 1 - b / 255
        min_cmy = min(c, m, y)
        c = (c - min_cmy) / (1 - min_cmy) * 100
        m = (m - min_cmy) / (1 - min_cmy) * 100
        y = (y - min_cmy) / (1 - min_cmy) * 100
        k = min_cmy * 100
        self.cmyk = (round(c, 2), round(m, 2), round(y, 2), round(k, 2))

    def _update_rgb_from_cmyk(self, c, m, y, k):
        c /= 100
        m /= 100
        y /= 100
        k /= 100
        r = 255 * (1 - c) * (1 - k)
        g = 255 * (1 - m) * (1 - k)
        b = 255 * (1 - y) * (1 - k)
        return int(r), int(g), int(b)

    def _update_hsv_from_rgb(self, r, g, b):
        h, s, v = colorsys.rgb_to_hsv(r/255, g/255, b/255)
        self.hsv = (int(h * 360), int(s * 100), int(v * 100))

