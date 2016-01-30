import sys
import termios
import colorama as colors
import string
from leap import Mouse

# Defaults
console_width = 104
controls = {
    'dynamic': 'Dynamic pointer control',
    'finger': 'Finger based pointer',
    'motion': 'Motion/gesture based pointer',
    'palm': 'Palm based pointer'
}
commands = {
    'help': 'List general help',
    'info': 'List current settings',
    'quit/exit': 'Quit the application'
}
customizations = {
    'aggression': 'Smoothing aggressiveness (INT)',
    'falloff': 'Smoothing falloff (FLOAT)',
    'width': 'Adjust console width (INT)'
}

# Initialize console colorization
colors.init(autoreset=True)
END = colors.Fore.RESET + colors.Style.RESET_ALL
CURSOR_UP_ONE = '\x1b[1A'
ERASE_LINE = '\x1b[2K'


class ColorUtil(object):
    def __init__(self):
        super(ColorUtil, self).__init__()

    @staticmethod
    def t(text, color):
        return color + text

    @staticmethod
    def w(text=''):
        return ColorUtil.t(text, colors.Fore.WHITE)

    @staticmethod
    def c(text=''):
        return ColorUtil.t(text, colors.Fore.CYAN)

    @staticmethod
    def b(text=''):
        return ColorUtil.t(text, colors.Fore.BLUE)

    @staticmethod
    def y(text=''):
        return ColorUtil.t(text, colors.Fore.YELLOW)

    @staticmethod
    def r(text=''):
        return ColorUtil.t(text, colors.Fore.RED)

    @staticmethod
    def m(text=''):
        return ColorUtil.t(text, colors.Fore.MAGENTA)

    @staticmethod
    def bl(text=''):
        return ColorUtil.t(text, colors.Fore.BLACK)


clr = ColorUtil


def spacer(wall=None, fill=' ', fill_color=clr.b()):
    if wall is None:
        wall = clr.w('|')
    return wall + fill_color + string.center('' + fill_color, console_width - 10, fill) + wall + END


def header(title=None, wall=None, fill='-', fill_color=clr.b()):
    if title is None:
        title = 'PyLeapMouse'
    if wall is None:
        wall = clr.w('.')
    return wall + fill_color + string.ljust(build_title(title) + fill_color, console_width, fill) + wall + END


def footer(title=None, wall=None, fill='-', fill_color=clr.b()):
    if title is None:
        title = 'PyLeapMouse'
    if wall is None:
        wall = clr.w('\'')
    return wall + fill_color + (build_title(title) + fill_color).ljust(console_width, fill) + wall + END


def heading(title='', wall=clr.w('|'), fill_color=clr.b(), fill='-',
            surround_left=clr.c('>=-'),
            surround_right=clr.c('-=<')):
    return wall + surround_left + fill_color \
           + (build_title(title) + fill_color).rjust(console_width - 6, fill) \
           + surround_right + wall + END


def build_title(title='',
                surround_left=clr.c('-=#[ '),
                surround_right=clr.c(' ]#=-')):
    return surround_left + title + surround_right


def build_definition(key='', value='', wall=clr.w('|'), fill_color=clr.w(),
                     fill='_', text_color=clr.y(), label_color=clr.y()):
    return wall + ' ' + label_color + key + fill_color + ' ' \
           + (' ' + text_color + value).rjust(console_width - len(key) - 13, fill) \
           + ' ' + wall + END


def build_status(value, key='', fill='.', wall=clr.w('|'), fill_color=clr.w(),
                 text_color=clr.y(), label_color=clr.y()):
    return wall + ' ' + label_color + (
            string.ljust(value, console_width + fill_color, fill)
            if key is '' or key is None else
            value + fill_color + ' ' + (' ' + text_color + key + fill_color).rjust(console_width - len(value) - 8, fill)) \
            + ' ' + wall + END


def build_error(message, title='ERROR'):
    return build_definition(title, message)


def build_warning(message, title='WARNING'):
    return build_definition(title, message)


def build_info(message, title='INFO'):
    return build_definition(title, message)


def show_help():
    print header()
    print "Use --finger (or blank) for pointer finger control, and --palm for palm control."
    print "Set smooth aggressiveness (# samples) with \"--smooth-aggressiveness [# samples]\""
    print "Set smooth falloff with \"--smooth-falloff [% per sample]\""
    print "Read README.md for even more info.\n"
    print footer()


def show_info(mode, title='Current Settings', wall=clr.w('|')):
    print spacer()
    print header(title, wall)
    show_status_dictionary({
        'aggression': str(mode.aggressiveness),
        'falloff': str(mode.falloff),
        'width': str(console_width),
    }, title, fill='-', fill_color=clr.m())
    show_status_dictionary({
        'screen width': str(Mouse.GetDisplayWidth()),
        'screen height': str(Mouse.GetDisplayHeight())
    }, 'Resolution')
    print spacer()
    print footer(title, wall)
    print spacer()


def show_dictionary(items, title='', wall=clr.w('|'), fill_color=clr.w(),
                    fill='_', text_color=clr.y(), label_color=clr.y()):
    print spacer()
    print heading(title)
    print spacer()
    for k, v in items.iteritems():
        print build_definition(k, v, wall, fill_color, fill, text_color, label_color)


def show_status_dictionary(items, title='', fill='.', wall=clr.w('|'), fill_color=clr.w(),
                           text_color=clr.y(), label_color=clr.y()):
    if title is not None and title is not '':
        print spacer()
        print heading(title)
        print spacer()
    for k, v in items.iteritems():
        print build_status(k, v, fill, wall, fill_color, text_color, label_color)


def console_help(control=None, wall=None):
    global controls, commands, customizations
    print header(control, wall)
    print spacer()
    if control is None:
        show_dictionary(controls, "Control Options")
        show_dictionary(commands, "Commands")
        show_dictionary(customizations, "Customizations")
    print spacer()
    print footer(control, wall)


def erase_line_up(n=1):
    i = 0
    while i < n:
        i += 1
        print CURSOR_UP_ONE + ERASE_LINE + CURSOR_UP_ONE


def get_input(prompt=''):
    response = raw_input(prompt)
    erase_line_up()
    # fd = sys.stdin
    # if fd.isatty():
    #     old = termios.tcgetattr(fd)
    #     new = termios.tcgetattr(fd)
    #     new[3] = new[3] & ~termios.ECHO
    #     try:
    #         termios.tcsetattr(fd, termios.TCSANOW, new)
    #         response = raw_input(prompt)
    #         print '\r          \r',
    #     finally:
    #         termios.tcsetattr(fd, termios.TCSANOW, old)
    # else:
    #     build_warning("Not a TTY")
    #     response = fd.readline().rstrip()
    return response


def stream_prime(count=1, wall=clr.w('|')):
    for i in range(count):
        print spacer(wall)


def stream_updates(data):
    erase_line_up(len(data))
    show_status_dictionary(data)
