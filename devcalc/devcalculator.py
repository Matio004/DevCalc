from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.graphics import Color, Rectangle
from kivy.core.clipboard import Clipboard

from systems import Hexadecimal, Decimal, Octal, Binary
from equation import Equation


# Label
class NumberView(Label):
    font_name = 'Roboto-Medium.ttf'

    def on_size(self, *args):
        self.canvas.before.clear()
        with self.canvas.before:
            Color(14 / 255, 23 / 255, 46 / 255, 18)
            Rectangle(pos=self.pos, size=self.size)

    def on_touch_down(self, touch):
        if self.collide_point(touch.pos[0], touch.pos[1]):
            Clipboard.copy(self.text)


class Calculator(GridLayout):
    # Keyboard layout
    layout = [
        ['A', 'B', 'C', 'D', 'E', 'F'],
        ['7', '8', '9', 'DEL', 'AC'],
        ['4', '5', '6', '*', '/'],
        ['1', '2', '3', '+', '-'],
        ['0', '=', 'Colors']
    ]

    # Basic presets
    equation = Equation()
    all_systems: tuple

    # Colors
    useful = '#00072B'
    unuseful = '#151D45'
    rest = '#267480'
    active = '#008035'
    label_color = '#0E172E'

    def __init__(self):
        super(Calculator, self).__init__(cols=1, size_hint=(1, 1), pos_hint={"left_x": 0, "left_y": 0}, spacing=3)
        system_box = GridLayout(cols=2, size_hint=(4, 4), spacing=3)

        hex_system = [Button(text='HEX', on_press=self.change_system, background_color=self.rest,
                             font_name='Roboto-Medium.ttf', width=70, size_hint=(.2, 1)), NumberView()]

        dec_system = [Button(text='DEC', on_press=self.change_system, background_color=self.rest,
                             font_name='Roboto-Medium.ttf', width=70, size_hint=(.2, 1)), NumberView()]

        oct_system = [Button(text='OCT', on_press=self.change_system, background_color=self.rest,
                             font_name='Roboto-Medium.ttf', width=70, size_hint=(.2, 1)), NumberView()]

        bin_system = [Button(text='BIN', on_press=self.change_system, background_color=self.rest,
                             font_name='Roboto-Medium.ttf', width=70, size_hint=(.2, 1)), NumberView()]

        self.all_systems = hex_system, dec_system, oct_system, bin_system

        for system in self.all_systems:
            for widget in system:
                system_box.add_widget(widget)

        self.add_widget(system_box)

        for raw in self.layout:
            box_raw = BoxLayout(orientation='horizontal', spacing=1)
            for symbol in raw:
                button = Button(text=symbol, on_press=self.callback, font_name='Roboto-Medium.ttf')
                box_raw.add_widget(button)
            self.add_widget(box_raw)

        self.show_useful_sings()
        self.set_all_systems()

    def change_system(self, instance):  # Changes system
        if instance.text == 'HEX':
            self.equation.set_system(Hexadecimal)
        elif instance.text == 'DEC':
            self.equation.set_system(Decimal)
        elif instance.text == 'OCT':
            self.equation.set_system(Octal)
        elif instance.text == 'BIN':
            self.equation.set_system(Binary)

        self.set_all_systems()
        self.show_useful_sings()

    def callback(self, instance):  # Gives correct label
        if self.equation.system == Hexadecimal:
            self.modify_text(instance)
        elif self.equation.system == Decimal:
            self.modify_text(instance)
        elif self.equation.system == Octal:
            self.modify_text(instance)
        elif self.equation.system == Binary:
            self.modify_text(instance)

    def modify_text(self, instance):
        """Add sights"""
        if instance.text == 'Colors':
            self.parent.parent.current = 'color'

        self.equation += instance.text if instance.text != '/' else '//'

        self.set_all_systems()

    def set_all_systems(self):
        """Show all"""
        # Hex
        self.all_systems[0][1].text = self.equation.get_hex()
        # Dec
        self.all_systems[1][1].text = self.equation.get_dec()
        # Oct
        self.all_systems[2][1].text = self.equation.get_oct()
        # Bin
        text = self.equation.get_bin()
        self.all_systems[3][1].text = (text[:39]+'\n'+text[40:] if text[0] != '-'
                                       else text[:40]+'\n'+text[41:])

    def show_useful_sings(self):
        # Keyboard
        for layout in self.children:
            if type(layout) == BoxLayout:
                for widget in layout.children:
                    if widget.text not in self.equation.system.symbols and widget.text not in \
                            ['*', '/', '+', '-', '=', self.layout[4][2], 'DEL', 'AC']:  # not useful
                        widget.background_color = self.unuseful
                    elif widget.text not in ['*', '/', '+', '-', '=', self.layout[4][2], 'DEL', 'AC']:  # useful
                        widget.background_color = self.useful
                    else:
                        widget.background_color = self.rest
        # Systems
        for system in self.all_systems:
            if system[0].text == self.equation.system.name:
                system[0].background_color = self.active
            else:
                system[0].background_color = self.rest
