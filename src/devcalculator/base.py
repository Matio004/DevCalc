from kivy.uix.label import Label
from kivy.graphics import Color, Rectangle
from kivy.core.clipboard import Clipboard


# Label
class NumberView(Label):
    font_name = './assets/Roboto-Medium.ttf'

    def on_size(self, *args):
        self.canvas.before.clear()
        with self.canvas.before:
            Color(14 / 255, 23 / 255, 46 / 255, 18)
            Rectangle(pos=self.pos, size=self.size)

    def on_touch_down(self, touch):
        if self.collide_point(touch.pos[0], touch.pos[1]):
            Clipboard.copy(self.text)
