from ...base.systems import System, Hexadecimal, Decimal, Octal, Binary


class Number:  # int is a bad idea
    __number = 0
    __sign = False  # False - positive True negative
    __system: System

    def __init__(self, value: int = 0, system: System = Hexadecimal):
        self.__number = value
        self.__system = system

        if self.__number < 0:
            self.__sign = True
            self.__number = -self.__number

    def append(self, literal):
        if literal in self.__system.symbols:
            self.__number *= self.__system.base
            self.__number += int(literal, self.__system.base)
            return self
        raise ValueError(f'Invalid literal for {self.__class__.__name__} with base {self.__system.base}: ', literal)

    def __repr__(self):
        return str(self.__number)

    def __index__(self):
        return self.__number

    def __add__(self, other):
        """+"""
        return self.__class__(self.__number + other.__number)

    def __sub__(self, other):
        """-"""
        return self.__class__(self.__number - other.__number)

    def __mul__(self, other):
        """*"""
        return self.__class__(self.__number * other.__number)

    def __floordiv__(self, other):
        """//"""
        return self.__class__(self.__number // other.__number)

    def __neg__(self):
        self.__number = ~self.__number + 1
        return self

    def __len__(self):
        return len(bin(self.__number)) - 2

    @property
    def value(self):
        return self.__number

    @property
    def system(self):
        return self.__system

    @system.setter
    def system(self, value):
        self.__system = value
