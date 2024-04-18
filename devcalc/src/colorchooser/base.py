from kivy.uix.label import Label
from kivy.graphics import Color, Rectangle
from kivy.core.clipboard import Clipboard

from ..base.functions import hex_color_fill, hex2rgb, int_color
from ..base.systems import RGB


class HEXNumber(Label):
    font_name = './assets/Roboto-Medium.ttf'

    def on_size(self, *args):
        self.canvas.before.clear()
        with self.canvas.before:
            Color(14 / 255, 23 / 255, 46 / 255, 1)
            Rectangle(pos=self.pos, size=self.size)

    def on_touch_down(self, touch):
        if self.collide_point(touch.pos[0], touch.pos[1]):
            Clipboard.copy('#' + hex_color_fill(self.text))


class RGBNumber(Label):
    font_name = './assets/Roboto-Medium.ttf'

    def __init__(self, label_id):
        super(RGBNumber, self).__init__()
        self.label_id = label_id

    def on_size(self, *args):
        self.canvas.before.clear()
        with self.canvas.before:
            Color(14 / 255, 23 / 255, 46 / 255, 18)
            Rectangle(pos=self.pos, size=self.size)

    def on_touch_down(self, touch):
        if self.collide_point(touch.pos[0], touch.pos[1]) and self.parent.parent.parent.equation.__system == RGB:
            self.parent.parent.parent.equation.__current_rgb_color = self.label_id
            self.parent.parent.parent.show_useful_sings()

    def change_color(self, color):
        self.canvas.before.clear()
        with self.canvas.before:
            color = int_color(hex2rgb(color))
            Color(color[0] / 255, color[1] / 255, color[2] / 255, 18)
            Rectangle(pos=self.pos, size=self.size)


class ColorLabel(Label):
    font_name = './assets/Roboto-Medium.ttf'

    def __init__(self, color):
        super(ColorLabel, self).__init__()
        self.virtual_color = color

    def on_size(self, *args):
        self.change_color(self.virtual_color)

    def on_touch_down(self, touch):
        if self.collide_point(touch.pos[0], touch.pos[1]):
            Clipboard.copy(', '.join(self.parent.parent.parent.equation.get_rgb()))

    def change_color(self, color):
        self.canvas.before.clear()
        with self.canvas.before:
            Color(int(color[0]) / 255, int(color[1]) / 255, int(color[2]) / 255, 1)
            Rectangle(pos=self.pos, size=self.size)
