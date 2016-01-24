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


def spacer(wall=clr.w('|'), fill=' ', fill_color=clr.b()):
    return wall + fill_color + string.center('' + fill_color, console_width - 30, fill) + wall + END


def header(title='PyLeapMouse', wall=clr.w('.'), fill='-', fill_color=clr.b()):
    return wall + fill_color + string.ljust(build_title(title) + fill_color, console_width, fill) + wall + END


def footer(title='PyLeapMouse', wall=clr.w('\''), fill='-', fill_color=clr.b()):
    return wall + fill_color + string.ljust(build_title(title) + fill_color, console_width, fill) + wall + END


def heading(title='', wall=clr.w('|'), fill_color=clr.b(), fill='-',
            surround_left=clr.c('>=-'),
            surround_right=clr.c('-=<')):
    return wall + surround_left + fill_color \
           + string.rjust(build_title(title) + fill_color, console_width - 6, fill) \
           + surround_right + wall + END


def build_title(title='',
                surround_left=clr.c('-=#[ '),
                surround_right=clr.c(' ]#=-')):
    return surround_left + title + surround_right


def build_definition(key='', value='', wall=clr.w('|'), fill_color=clr.w(),
                     fill='_', text_color=clr.y(), label_color=clr.y()):
    return wall + ' ' + label_color + key + fill_color + ' ' \
           + string.rjust(' ' + text_color + value, console_width - len(key) - 13, fill) \
           + ' ' + wall + END


def build_error(message, title='ERROR'):
    return build_definition(title, message)


def build_warning(message, title='WARNING'):
    return build_definition(title, message)


def build_info(message, title='INFO'):
    return build_definition(title, message)


def build_status_message(key='', value='', fill='_', wall=clr.w('|'), fill_color=clr.w(),
                         text_color=clr.y(), label_color=clr.y()):
    return wall + ' ' + label_color + value + fill_color + ' ' \
           + (string.ljust(' ' + text_color + key + fill_color, console_width - len(value) - 8, fill)
              if key is '' or key is None else
              string.rjust(' ' + text_color + key + fill_color, console_width - len(value) - 8, fill)) + ' ' \
           + wall + END


def build_status(message, title=''):
    return build_status_message(title, message, '.')


def show_help():
    print header()
    print "Use --finger (or blank) for pointer finger control, and --palm for palm control."
    print "Set smooth aggressiveness (# samples) with \"--smooth-aggressiveness [# samples]\""
    print "Set smooth falloff with \"--smooth-falloff [% per sample]\""
    print "Read README.md for even more info.\n"
    print footer()


def show_info(mode, title='Current Settings'):
    # header()
    show_status_dictionary({
        'aggression': str(mode.aggressiveness),
        'falloff': str(mode.falloff),
        'width': str(console_width),
    }, title)
    show_status_dictionary({
        'screen width': str(Mouse.GetDisplayWidth()),
        'screen height': str(Mouse.GetDisplayHeight())
    }, 'Resolution')
    # footer()


def show_dictionary(items, title=''):
    print heading(title)
    for k, v in items.iteritems():
        print build_definition(k, v)


def show_status_dictionary(items, title=''):
    print heading(title)
    for k, v in items.iteritems():
        print build_status(k, v)


def console_help(control=None):
    global controls, commands, customizations
    print header()
    if control is None:
        show_dictionary(controls, "Control Options")
        show_dictionary(commands, "Commands")
        show_dictionary(customizations, "Customizations")
    print footer()


def get_input(prompt=''):
    fd = sys.stdin
    if fd.isatty():
        old = termios.tcgetattr(fd)
        new = termios.tcgetattr(fd)
        new[3] = new[3] & ~termios.ECHO
        try:
            termios.tcsetattr(fd, termios.TCSANOW, new)
            response = raw_input(prompt)
            print '\r          \r',
        finally:
            termios.tcsetattr(fd, termios.TCSANOW, old)
    else:
        build_warning("Not a TTY")
        response = fd.readline().rstrip()
    return response
