from PIL import ImageColor


def encrypt(string, length):
    """Split string by length"""
    return ' '.join(string[i:i+length] for i in range(0, len(string), length))


def hex_color_fill(string):
    """Fill hex string add 0 and #"""
    for _ in range(6-len(string)):
        string += '0'
    string = string.replace(' ', '')
    return string.strip('#')


def rgb_color_fill(_list):
    """Fill rgb list add 0"""
    _list = list(map(str, _list))
    for item in range(len(_list)):
        if len(_list[item]) == 0:
            _list[item] += '0'
    return _list


def rgb2hex(sequence):
    """From rgb to hex"""
    sequence = [int(num) for num in sequence]
    return "{:02x}{:02x}{:02x}".format(sequence[0], sequence[1], sequence[2])


def hex2rgb(hex_code):
    """From hex to rgb"""
    return [str(color) for color in ImageColor.getrgb('#'+hex_code if hex_code[0] != '#'else hex_code)]


def int_color(sequence):
    """Rgb list 3string to list 3int"""
    return list(map(int, sequence))


def r_encrypt(string: str, length: int):
    # string reverse, slice, reverse sliced
    _list = [string[::-1][i:i + length][::-1] for i in range(0, len(string), length)]
    _list.reverse()
    if len(_list) == 0:
        _list = ['0']
    return ' '.join(_list)


def fill_binary(string: str, split):
    string = string.split(' ')
    string[0] = (split - len(string[0]))*'0'+string[0]
    return r_encrypt(''.join(string), split)
