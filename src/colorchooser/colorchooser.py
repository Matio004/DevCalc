from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout

from .equation import ColorEquation
from ..base.systems import Hexadecimal, RGB
from ..base.functions import hex_color_fill, hex2rgb
from .base import HEXNumber, RGBNumber, ColorLabel


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
    useful = '#151D45'  # '#00072B'
    unuseful = '#00072B'  # '#151D45'
    rest = '#267480'
    active = '#008035'
    label_color = '#0E172E'

    # font
    font_name = './assets/Roboto-Medium.ttf'

    def __init__(self):
        super(ColorChooser, self).__init__(cols=1, size_hint=(1, 1), pos_hint={"left_x": 0, "left_y": 0}, spacing=3)
        system_box = GridLayout(cols=1, size_hint=(4, 4), spacing=3)

        hex_system = [Button(text='HEX', on_press=self.change_system, background_color=self.rest,
                             font_name=self.font_name), HEXNumber(), ColorLabel([0, 0, 0])]
        rgb_system = [Button(text='RGB', on_press=self.change_system, background_color=self.rest,
                             font_name=self.font_name), RGBNumber(0), RGBNumber(1), RGBNumber(2)]

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
                button = Button(text=symbol, on_press=self.call_back, font_name=self.font_name)
                box_raw.add_widget(button)
            self.add_widget(box_raw)

        self.show_useful_sings()
        self.set_all_systems()

    def change_system(self, instance):  # Changes __system
        if instance.text == 'HEX':
            self.equation.system = Hexadecimal
        elif instance.text == 'RGB':
            self.equation.system = RGB

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

    def modify_color(self):  # todo fill background behind hex
        if self.equation.system == Hexadecimal:
            self.all_systems[0][2].change_color(hex2rgb(hex_color_fill(self.equation.get_hex())))
            # self.all_systems[0][1].change_color(hex2rgb(hex_color_fill(self.equation.get_hex())))
        else:
            self.all_systems[0][2].change_color(self.equation.get_int_rgb()[:])
            # self.all_systems[0][1].change_color(self.equation.get_int_rgb()[:])

    def set_all_systems(self):  # todo add R G B prefixes
        color = 0

        self.all_systems[0][1].text = self.equation.get_hex()  # Hex label
        for label in self.all_systems[1][1:]:
            label.text = str(self.equation.get_rgb()[color])
            color += 1

    def show_useful_sings(self):
        # Keyboard
        for layout in self.children:
            if isinstance(layout, BoxLayout):
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
