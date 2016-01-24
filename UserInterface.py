import colorama as colors
import string

# Defaults
console_width = 104
controls = {
    'dynamic':      'Dynamic pointer control',
    'finger':       'Finger based pointer',
    'motion':       'Motion/gesture based pointer',
    'palm':         'Palm based pointer'
}
commands = {
    'help':         'List general help',
    'info':         'List current settings',
    'quit':         'Quit the application'
}
customizations = {
    'aggression':   'Smoothing aggressiveness (INT)',
    'falloff':      'Smoothing falloff (FLOAT)',
    'width':        'Adjust console width (INT)'
}


# Initialize console colorization
colors.init(autoreset=True)
HEADER = colors.Fore.GREEN
TITLE = colors.Fore.CYAN
MESSAGE = colors.Fore.BLUE
ERROR = colors.Fore.RED
WARNING = colors.Fore.YELLOW
INFO = colors.Fore.WHITE
BLUE = colors.Fore.BLUE
CYAN = colors.Fore.CYAN
WHITE = colors.Fore.WHITE
YELLOW = colors.Fore.YELLOW
END = colors.Fore.RESET + colors.Style.RESET_ALL
#  White             Blue            Cyan
APOS_WHITE,         APOS_BLUE,      APOS_CYAN = \
    WHITE + '\'',   BLUE + '\'',    CYAN + '\''
BAR_WHITE,          BAR_BLUE,       BAR_CYAN = \
    WHITE + '|',    BLUE + '|',     CYAN + '|'
OPEN_WHITE,         OPEN_BLUE,      OPEN_CYAN = \
    WHITE + '[',    BLUE + '[',     CYAN + '['
CLOSE_WHITE,        CLOSE_BLUE,     CLOSE_CYAN = \
    WHITE + ']',    BLUE + ']',     CYAN + ']'
LT_WHITE,           LT_BLUE,        LT_CYAN = \
    WHITE + '<',    BLUE + '<',     CYAN + '<'
GT_WHITE,           GT_BLUE,        GT_CYAN = \
    WHITE + '>',    BLUE + '>',     CYAN + '>'
DASH_WHITE,         DASH_BLUE,      DASH_CYAN = \
    WHITE + '-',    BLUE + '-',     CYAN + '-'
DOT_WHITE,          DOT_BLUE,       DOT_CYAN = \
    WHITE + '.',    BLUE + '.',     CYAN + '.'
EQUAL_WHITE,        EQUAL_BLUE,     EQUAL_CYAN = \
    WHITE + '=',    BLUE + '=',     CYAN + '='
HASH_WHITE,         HASH_BLUE,      HASH_CYAN = \
    WHITE + '#',    BLUE + '#',     CYAN + '#'


def header(title='PyLeapMouse'):
    print DOT_WHITE + DASH_CYAN + EQUAL_CYAN + EQUAL_CYAN + BLUE \
        + string.center(build_title(title) + BLUE, console_width, '=') \
        + EQUAL_CYAN + EQUAL_CYAN + DASH_CYAN + DOT_WHITE + END


def footer(title='PyLeapMouse'):
    print APOS_WHITE + DASH_CYAN + EQUAL_CYAN + EQUAL_CYAN + BLUE \
        + string.center(build_title(title) + BLUE, console_width, '=') \
        + EQUAL_CYAN + EQUAL_CYAN + DASH_CYAN + APOS_WHITE + END


def heading(title=''):
    print BAR_WHITE + BLUE \
        + string.center('' + BLUE, console_width - 24, ' ') \
        + BAR_WHITE + END
    print BAR_WHITE + GT_CYAN + EQUAL_CYAN + DASH_CYAN + BLUE \
        + string.center(build_title(title) + BLUE, console_width, '-') \
        + DASH_CYAN + EQUAL_CYAN + LT_CYAN + BAR_WHITE + END


def build_title(title=''):
    return DASH_CYAN + EQUAL_CYAN + HASH_CYAN + '[ ' + title + ' ]' + HASH_CYAN + EQUAL_CYAN + DASH_CYAN


def build_definition(key='', value=''):
    prefix = BAR_WHITE + ' ' + string.ljust(YELLOW + key + WHITE + ' ', 14, '.')
    target_len = console_width - len(prefix) - 9
    suffix = string.rjust(' ' + YELLOW + value, target_len, '.') + ' ' + BAR_WHITE + END
    return prefix + suffix


def build_error(message, title='ERROR'):
    header(title)
    print build_definition(title, message)
    footer(title)


def show_help():
    header()
    print "Use --finger (or blank) for pointer finger control, and --palm for palm control."
    print "Set smooth aggressiveness (# samples) with \"--smooth-aggressiveness [# samples]\""
    print "Set smooth falloff with \"--smooth-falloff [% per sample]\""
    print "Read README.md for even more info.\n"
    footer()


def show_info(mode, title='Current Settings'):
    header()
    build_dictionary({
        'aggression':   str(mode.aggressiveness),
        'falloff':      str(mode.falloff),
        'width':        str(console_width)
    }, title)
    footer()


def build_dictionary(items, title=''):
    heading(title)
    for k, v in items.iteritems():
        print build_definition(k, v)


def console_help(control=None):
    global controls, commands, customizations
    header()
    if control is None:
        build_dictionary(controls, "Control Options")
        build_dictionary(commands, "Commands")
        build_dictionary(customizations, "Customizations")
    footer()
