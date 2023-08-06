'''colorful commandline
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~'''

class COLORS:
    BLACK = 30
    GRAY = 30
    RED = 31
    GREEN = 32
    YELLOW = 33
    BLUE = 34
    MAGENTA = 35
    CYAN = 36
    LIGHT_GRAY = 37
    DARK_GRAY = 90
    LIGHT_RED = 91
    LIGHT_GREEN = 92
    LIGHT_YELLOW = 93
    LIGHT_BLUE = 94
    LIGHT_MAGENTA = 95
    LIGHT_CYAN = 96
    WHITE = 97

    ERROR = RED
    SUCCESS = GREEN
    WARNING = YELLOW
    MINOR = LIGHT_GRAY

class cstring:
    """ make colored string for command line
    Args:
        rawstring (str): raw string
        color (str, optional): set color code
        using preset, use static constant of COLOR
    """

    def __init__(self, rawstring: str, color: int):
        self.rawstring = rawstring
        self.color = color

    @property
    def string(self):
        if self.color == 0:
            return self.rawstring
        else:
            return f'\033[{self.color}m{self.rawstring}\033[0m'

    def set_success(self):
        self.color = COLORS.SUCCESS
        return self.string

    def set_error(self):
        self.color = COLORS.ERROR
        return self.string

    def set_warning(self):
        self.color = COLORS.WARNING
        return self.string

    def set_minor(self):
        self.color = COLORS.MINOR
        return self.string

def cprint(string: str, color: int):
    """cprint

    print colored string

    Args:
        string (str): string to be colored 
        color (int): color (preset or not preset)
    """
    print(cstring(string, color).string, end='')
