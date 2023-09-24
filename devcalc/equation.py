from systems import Hexadecimal, RGB, System, Decimal, Octal, Binary
from base import encrypt, rgb_color_fill, hex_color_fill, hex2rgb, rgb2hex, int_color, r_encrypt, fill_binary


class Equation:
    system = Hexadecimal

    def __init__(self):
        self.__raw_equation = ''  # Equation
        self.__int_string = ''  # Int decimal
        self.__string = ''  # Current number

    # +
    def __add__(self, other: str):
        """Add sight to equation"""
        if len(''.join(self.get_bin().strip().lstrip('-0').split())) < 64:
            if other in self.system.symbols:  # if number
                self.__string += other
            elif other in System.equations[0]:  # if + - * /
                self.__raw_equation += self.__int_string + other
                self.__string = ''
            elif other == '=':
                self.__raw_equation += self.__int_string
                self.update()
        if other in System.equations[1]:  # if AC DEL
            if other == 'AC':
                self.__del__()
            elif other == 'DEL':
                self.__string = self.__string[:-1]
        self.int()
        return self

    def int(self):
        """String to __int_string"""
        try:
            self.__int_string = str(int(self.__string, self.system.base))
        except ValueError:
            self.__int_string = ''
        return self.__int_string

    def get_hex(self):
        """Get hex number"""
        try:
            return r_encrypt(str(hex(int(self.__int_string)))[2:].upper(), Hexadecimal.split)\
                if int(self.__int_string) >= 0\
                else '-' + r_encrypt(str(hex((int(self.__int_string))))[3:].upper(), Hexadecimal.split)
        except ValueError:
            return '0'

    def get_dec(self):
        """Get dec number"""
        return r_encrypt(self.__int_string, Decimal.split)

    def get_oct(self):
        """Get oct number"""
        try:
            return r_encrypt(str(oct(int(self.__int_string)))[2:], Octal.split)\
                if int(self.__int_string) >= 0 else '-' + r_encrypt(str(oct((int(self.__int_string))))[3:], Octal.split)
        except ValueError:
            return '0'

    def get_bin(self):
        """Get bin number"""
        try:
            return fill_binary(r_encrypt(str(bin((int(self.__int_string))))[2:], Binary.split), Binary.split)\
                if int(self.__int_string) >= 0\
                else '-' + fill_binary(r_encrypt(str(bin((int(self.__int_string))))[3:], Binary.split), Binary.split)
        except ValueError:
            return '0000'

    def set_system(self, system):
        """Set number system"""
        try:
            self.__string = str(system.function(int(self.__string, self.system.base)))
        except ValueError:
            self.__string = ''

        self.system = system
        self.__raw_equation = ''

    def __del__(self):
        self.__raw_equation = ''
        self.__int_string = ''
        self.__string = ''

    def update(self):
        """Evaluate equation"""
        try:
            self.__string = str(self.system.function((eval(self.__raw_equation))))
            self.__raw_equation = ''
        except SyntaxError:
            pass


class ColorEquation:
    system = Hexadecimal

    def __init__(self):
        self.__hex_equation = ''
        self.__rgb_equation = ['0', '0', '0']
        self.current_rgb_color = 0

    def __add__(self, other: str):
        if self.system == Hexadecimal and other in Hexadecimal.symbols:
            if len(self.__hex_equation) < 6:
                self.__hex_equation += other

        elif self.system == RGB and other in RGB.symbols:
            self.update_color()
            # rgb should be str not int
            if len(self.__rgb_equation[self.current_rgb_color]) < 3:
                if int(self.__rgb_equation[self.current_rgb_color]+other) <= 255:
                    if int(self.__rgb_equation[self.current_rgb_color]) == 0:
                        self.__rgb_equation[self.current_rgb_color] = ''
                    self.__rgb_equation[self.current_rgb_color] = self.__rgb_equation[self.current_rgb_color]+other

        # Deletion
        if other == 'AC':
            self.__del__()
        elif other == 'DEL':
            self.__hex_equation = self.__hex_equation[:-1]
            self.__rgb_equation[self.current_rgb_color] = self.__rgb_equation[self.current_rgb_color][:-1]

        self.update()
        return self

    def __del__(self):
        self.__hex_equation = ''

        self.__rgb_equation = ['0', '0', '0']

    def set_system(self, system):
        self.__del__()
        self.system = system

    def set_color(self, color):
        self.current_rgb_color = color

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
        """Set other system"""
        if self.system == Hexadecimal:
            self.__rgb_equation = hex2rgb(hex_color_fill(self.__hex_equation))
        elif self.system == RGB:
            self.__hex_equation = rgb2hex(rgb_color_fill(self.__rgb_equation[:]))

    def update_color(self):
        for color in range(len(self.__rgb_equation)):
            if len(self.__rgb_equation[color]) <= 0:
                self.__rgb_equation[color] = '0'
