# William Yager
# Leap Python mouse controller POC
import string
import sys
import colorama as colors
from MouseMode import MouseMode
from leap import Leap, Mouse
from PalmControl import PalmControlListener  # For palm-tilt based control
from FingerControl import FingerControlListener  # For finger-pointing control
from MotionControl import MotionControlListener  # For motion control
from DynamicControl import DynamicControlListener  # For dynamic controls

# Initialize console colorization
colors.init(autoreset=True)
HEADER = colors.Fore.GREEN
TITLE = colors.Fore.CYAN
MESSAGE = colors.Fore.BLUE
ERROR = colors.Fore.RED
WARNING = colors.Fore.YELLOW
INFO = colors.Fore.WHITE
END = colors.Fore.RESET + colors.Style.RESET_ALL
console_width = 80


def header(title='PyLeapMouse'):
    print colors.Fore.WHITE + '.' \
          + colors.Fore.CYAN + '-==' \
          + colors.Fore.BLUE \
          + string.center(build_title(title) + colors.Fore.BLUE, console_width, '=') \
          + colors.Fore.CYAN + '==-' \
          + colors.Fore.WHITE + '.' \
          + END


def footer(title='PyLeapMouse'):
    print colors.Fore.WHITE + '\'' \
          + colors.Fore.CYAN + '-==' \
          + colors.Fore.BLUE \
          + string.center(build_title(title) + colors.Fore.BLUE, console_width, '=') \
          + colors.Fore.CYAN + '==-' \
          + colors.Fore.WHITE + '\'' \
          + END


def heading(title=''):
    print colors.Fore.WHITE + '|' \
          + colors.Fore.BLUE \
          + string.center('' + colors.Fore.BLUE, console_width - 18, ' ') \
          + colors.Fore.WHITE + '|' \
          + END
    print colors.Fore.WHITE + '|' \
          + colors.Fore.CYAN + '-=-' \
          + colors.Fore.BLUE \
          + string.center(build_title(title) + colors.Fore.BLUE, console_width, '-') \
          + colors.Fore.CYAN + '-=-' \
          + colors.Fore.WHITE + '|' \
          + END


def build_title(title=''):
    return colors.Fore.CYAN + '-=#' \
           + colors.Style.DIM + colors.Fore.CYAN \
           + '[ ' + title + ' ]' \
           + colors.Style.NORMAL + colors.Fore.CYAN + '#=-'


def build_definition(key='', value=''):
    prefix = colors.Fore.WHITE + '| ' + string.ljust(colors.Fore.YELLOW + key + colors.Fore.WHITE + ' ', 14, '.')
    target_len = console_width - len(prefix) - 3
    suffix = string.rjust(' ' + colors.Fore.YELLOW + value, target_len, '.') + colors.Fore.WHITE + ' |' + END
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


def console_help(control=None):
    header()
    if control is None:
        heading("Control Options")
        print build_definition('dynamic', 'dynamic pointer control')
        print build_definition('finger', 'finger based pointer')
        print build_definition('motion', 'motion/gesture pointer')
        print build_definition('palm', 'palm based pointer')
        heading("Commands")
        print build_definition('help', 'display this help list')
        print build_definition('    ', '(Optional: command target)')
        print build_definition('quit', 'exit PyLeapMouse')
        heading("Customizations")
        print build_definition('aggression', 'Smoothing aggressiveness value (INT)')
        print build_definition('falloff', 'Smoothing falloff value (FLOAT)')
        print build_definition('width', 'Adjust console width (INT)')
    footer()


def main():
    if "-h" in sys.argv or "--help" in sys.argv:
        show_help()
        return

    # Defaults
    mode = MouseMode()
    listener = None

    # Process command line arguments
    for i in range(0, len(sys.argv)):
        arg = sys.argv[i].lower()
        if "--dynamic" in arg:
            mode.set_mode(MouseMode.MODE_DYNAMIC)
        if "--finger" in arg:
            mode.set_mode(MouseMode.MODE_FINGER)
        if "--motion" in arg:
            mode.set_mode(MouseMode.MODE_MOTION)
        if "--palm" in arg:
            mode.set_mode(MouseMode.MODE_PALM)
        if "--smooth-falloff" in arg:
            mode.set_falloff(float(sys.argv[i + 1]))
        if "--smooth-aggressiveness" in arg:
            mode.set_aggressiveness(int(sys.argv[i + 1]))

    # Display the initial help content
    console_help()

    # Get a Leap controller
    controller = Leap.Controller()
    controller.set_policy_flags(Leap.Controller.POLICY_BACKGROUND_FRAMES)

    # Input loop
    while True:
        if listener is not None:
            # Remove previous listener
            controller.remove_listener(listener)
        # Define the listener object which controls the mouse
        try:
            if mode.is_dynamic():  # Dynamic pointer mode
                listener = DynamicControlListener(
                        Mouse,
                        aggressiveness=mode.get_aggressiveness(),
                        falloff=mode.get_falloff()
                )
                print "Using dynamic mode..."
            elif mode.is_finger():  # Finger pointer mode
                listener = FingerControlListener(
                        Mouse,
                        aggressiveness=mode.get_aggressiveness(),
                        falloff=mode.get_falloff()
                )
                print "Using finger mode..."
            elif mode.is_palm():  # Palm control mode
                listener = PalmControlListener(Mouse)
                print "Using palm mode..."
            elif mode.is_motion():  # Motion control mode
                listener = MotionControlListener(Mouse)
                print "Using motion mode..."
            elif mode.is_none():  # Mode is not set
                print "Unset mode..."
                break
        except Exception as e:
            build_error('{}'.format(e.message))

        print "Adding Listener."
        controller.add_listener(listener)  # Attach the listener

        # Display options menu and await input
        mode = prompt(mode)

    if listener is not None:
        # Remove the listener when done
        controller.remove_listener(listener)


def prompt(mode):
    global console_width
    # Keep this process running until Enter is pressed
    choice = sys.stdin.readline()
    if "dynamic" in choice:
        mode.set_mode(MouseMode.MODE_DYNAMIC)
    if "finger" in choice:
        mode.set_mode(MouseMode.MODE_FINGER)
    if "motion" in choice:
        mode.set_mode(MouseMode.MODE_MOTION)
    if "palm" in choice:
        mode.set_mode(MouseMode.MODE_PALM)
    if "quit" in choice:
        mode.set_mode(None)
    if "falloff" in choice:
        key, value = choice.split(' ', 1)
        mode.set_falloff(float(value))
    if "aggression" in choice:
        key, value = choice.split(' ', 1)
        mode.set_aggressiveness(int(value))
    if "width" in choice:
        key, value = choice.split(' ', 1)
        console_width = int(value)
        print 'Updated console width to: {}'.format(value)
    if "help" in choice:
        if " " in choice:
            key, value = choice.split(' ', 1)
            console_help(control=value)
        else:
            console_help()
    return mode

main()
