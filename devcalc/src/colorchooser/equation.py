from ..base.systems import Hexadecimal, RGB
from ..base.functions import encrypt, rgb_color_fill, hex_color_fill, hex2rgb, rgb2hex, int_color


class ColorEquation:
    __system = Hexadecimal

    __hex_equation = ''
    __rgb_equation = ['0', '0', '0']
    __current_rgb_color = 0

    def __add__(self, other: str):
        if self.__system == Hexadecimal and other in Hexadecimal.symbols:
            if len(self.__hex_equation) < 6:
                self.__hex_equation += other

        elif self.__system == RGB and other in RGB.symbols:
            self.update_color()
            # rgb should be str not int
            if len(self.__rgb_equation[self.__current_rgb_color]) < 3:
                if int(self.__rgb_equation[self.__current_rgb_color] + other) <= 255:
                    if int(self.__rgb_equation[self.__current_rgb_color]) == 0:
                        self.__rgb_equation[self.__current_rgb_color] = ''
                    self.__rgb_equation[self.__current_rgb_color] = self.__rgb_equation[self.__current_rgb_color] + other

        # Deletion
        if other == 'AC':
            self.__clear()
        elif other == 'DEL':
            self.__hex_equation = self.__hex_equation[:-1]
            self.__rgb_equation[self.__current_rgb_color] = self.__rgb_equation[self.__current_rgb_color][:-1]

        self.update()
        return self

    def __clear(self):
        self.__hex_equation = ''

        self.__rgb_equation = ['0', '0', '0']

    @property
    def system(self):
        return self.__system

    @system.setter
    def system(self, value):
        self.__clear()
        self.__system = value

    @property
    def current_rgb_color(self):
        return self.__current_rgb_color

    @current_rgb_color.setter
    def current_rgb_color(self, value):
        self.__current_rgb_color = value

    def get_hex(self):
        """Get hex format: #rrggbb"""
        return '#'+encrypt(hex_color_fill(self.__hex_equation), 2).upper()

    def get_rgb(self):
        """Get rgb format: [rrr, ggg, bbb] in list[str, str, str]"""
        return rgb_color_fill(self.__rgb_equation[:])

    def get_int_rgb(self):
        """Get rgb format: [rrr, ggg, bbb] in list[int, int, int]"""
        return int_color(rgb_color_fill(self.__rgb_equation[:]))

    def update(self):
        """Set other __system"""
        if self.__system == Hexadecimal:
            self.__rgb_equation = hex2rgb(hex_color_fill(self.__hex_equation))
        elif self.__system == RGB:
            self.__hex_equation = rgb2hex(rgb_color_fill(self.__rgb_equation[:]))

    def update_color(self):
        for color in range(len(self.__rgb_equation)):
            if len(self.__rgb_equation[color]) <= 0:
                self.__rgb_equation[color] = '0'
