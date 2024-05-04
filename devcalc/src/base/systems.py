import numpy


class System:
    name: str
    symbols: list
    equations: list = ['+ - * //'.split(), 'DEL AC'.split()]
    base: int
    function: classmethod
    split: int


class Hexadecimal(System):
    name = 'HEX'
    symbols = '0 1 2 3 4 5 6 7 8 9 A B C D E F'.split()
    base = 16
    function = hex
    split = 4


class Decimal(System):
    name = 'DEC'
    symbols = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    base = 10
    function = int
    split = 3


class Octal(System):
    name = 'OCT'
    symbols = '0 1 2 3 4 5 6 7'.split()
    base = 8
    function = oct
    split = 3


class Binary(System):
    name = 'BIN'
    symbols = ['0', '1']
    base = 2
    function = lambda x: numpy.binary_repr(x, 64)
    split = 4


class RGB(Decimal):
    name = 'RGB'
