from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.graphics import Color, Rectangle
from kivy.core.clipboard import Clipboard

from equation import ColorEquation
from systems import Hexadecimal, RGB
from base import hex_color_fill, hex2rgb, int_color


class HEXNumber(Label):
    font_name = 'Roboto-Medium.ttf'

    def on_size(self, *args):
        self.canvas.before.clear()
        with self.canvas.before:
            Color(14 / 255, 23 / 255, 46 / 255, 18)
            Rectangle(pos=self.pos, size=self.size)

    def on_touch_down(self, touch):
        if self.collide_point(touch.pos[0], touch.pos[1]):
            Clipboard.copy('#' + hex_color_fill(self.text))


class RGBNumber(Label):
    font_name = 'Roboto-Medium.ttf'

    def __init__(self, label_id):
        super(RGBNumber, self).__init__()
        self.label_id = label_id

    def on_size(self, *args):
        self.canvas.before.clear()
        with self.canvas.before:
            Color(14 / 255, 23 / 255, 46 / 255, 18)
            Rectangle(pos=self.pos, size=self.size)

    def on_touch_down(self, touch):
        if self.collide_point(touch.pos[0], touch.pos[1]) and self.parent.parent.parent.equation.system == RGB:
            self.parent.parent.parent.equation.current_rgb_color = self.label_id
            self.parent.parent.parent.show_useful_sings()

    def change_color(self, color):
        self.canvas.before.clear()
        with self.canvas.before:
            color = int_color(hex2rgb(color))
            Color(color[0] / 255, color[1] / 255, color[2] / 255, 18)
            Rectangle(pos=self.pos, size=self.size)


class ColorLabel(Label):
    font_name = 'Roboto-Medium.ttf'

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


class ColorChooser(GridLayout):
    # Layout
    layout = [
        ['C', 'D', 'E', 'F'],
        ['8', '9', 'A', 'B'],
        ['4', '5', '6', '7'],
        ['0', '1', '2', '3'],
        ['AC', 'DEL', 'Calculator']
    ]

    # Basic presets
    equation = ColorEquation()
    all_systems: tuple

    # Colors
    useful = '#00072B'
    unuseful = '#151D45'
    rest = '#267480'
    active = '#008035'
    label_color = '#0E172E'

    def __init__(self):
        super(ColorChooser, self).__init__(cols=1, size_hint=(1, 1), pos_hint={"left_x": 0, "left_y": 0}, spacing=3)
        system_box = GridLayout(cols=1, size_hint=(4, 4), spacing=3)

        hex_system = [Button(text='HEX', on_press=self.change_system, background_color=self.rest,
                             font_name='Roboto-Medium.ttf'), HEXNumber(), ColorLabel([0, 0, 0])]
        rgb_system = [Button(text='RGB', on_press=self.change_system, background_color=self.rest,
                             font_name='Roboto-Medium.ttf'), RGBNumber(0), RGBNumber(1), RGBNumber(2)]

        self.all_systems = hex_system, rgb_system

        for system in self.all_systems:
            box_raw = BoxLayout(orientation='horizontal', spacing=3)
            for widget in system:
                box_raw.add_widget(widget)
            system_box.add_widget(box_raw)

        self.add_widget(system_box)

        for raw in self.layout:
            box_raw = BoxLayout(orientation='horizontal', spacing=1)
            for symbol in raw:
                button = Button(text=symbol, on_press=self.call_back, font_name='Roboto-Medium.ttf')
                box_raw.add_widget(button)
            self.add_widget(box_raw)

        self.show_useful_sings()
        self.set_all_systems()

    def change_system(self, instance):  # Changes system
        if instance.text == 'HEX':
            self.equation.set_system(Hexadecimal)
        elif instance.text == 'RGB':
            self.equation.set_system(RGB)

        self.set_all_systems()
        self.modify_color()
        self.show_useful_sings()

    def call_back(self, instance):
        if self.equation.system == Hexadecimal:
            self.modify_text(instance)
        elif self.equation.system == RGB:
            self.modify_text(instance)
        self.modify_color()

    def modify_text(self, instance):
        # DevCalc screen
        if instance.text == self.layout[4][2]:  # switch to calc
            self.parent.parent.current = 'calc'

        self.equation += instance.text

        self.set_all_systems()

    def modify_color(self):
        if self.equation.system == Hexadecimal:
            self.all_systems[0][2].change_color(hex2rgb(hex_color_fill(self.equation.get_hex())))
        else:
            self.all_systems[0][2].change_color(self.equation.get_int_rgb()[:])

    def set_all_systems(self):
        color = 0

        self.all_systems[0][1].text = self.equation.get_hex()  # Hex label
        for label in self.all_systems[1][1:]:
            label.text = str(self.equation.get_rgb()[color])
            color += 1

    def show_useful_sings(self):
        # Keyboard
        for layout in self.children:
            if type(layout) == BoxLayout:
                for widget in layout.children:
                    # not useful
                    if widget.text not in self.equation.system.symbols \
                            and widget.text not in ['AC', 'DEL', self.layout[4][2]]:
                        widget.background_color = self.unuseful
                    elif widget.text not in ['AC', 'DEL', self.layout[4][2]]:  # useful
                        widget.background_color = self.useful
                    else:
                        widget.background_color = self.rest

        # System
        for system in self.all_systems:
            if system[0].text == self.equation.system.name:
                system[0].background_color = self.active
            else:
                system[0].background_color = self.rest

        for rgb_label in self.all_systems[1][1:]:
            if rgb_label.label_id == self.equation.current_rgb_color and self.equation.system == RGB:
                rgb_label.change_color(self.active)
            else:
                rgb_label.change_color(self.label_color)
