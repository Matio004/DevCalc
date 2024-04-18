from ..base.systems import Hexadecimal, System, Decimal, Octal, Binary
from ..base.functions import r_encrypt, fill_binary


class Equation:
    __system = Hexadecimal

    # def __init__(self):
    __raw_equation = ''  # Equation
    __int_string = ''  # Int decimal
    __string = ''  # Current number

    # +
    def __add__(self, other: str):
        """Add sight to equation"""
        if len(''.join(self.get_bin().strip().lstrip('-0').split())) < 64:
            if other in self.__system.symbols:  # if number
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
            self.__int_string = str(int(self.__string, self.__system.base))
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

    @property
    def system(self):
        return self.__system

    @system.setter
    def system(self, value):
        """Set number __system"""
        try:
            self.__string = str(value.function(int(self.__string, self.__system.base)))
        except ValueError:
            self.__string = ''

        self.__system = value
        self.__raw_equation = ''

    def __del__(self):
        self.__raw_equation = ''
        self.__int_string = ''
        self.__string = ''

    def update(self):
        """Evaluate equation"""
        try:
            self.__string = str(self.__system.function((eval(self.__raw_equation))))
            self.__raw_equation = ''
        except SyntaxError:
            pass
