# William Yager
# Leap Python mouse controller POC
import sys
from leap import Leap, Mouse
from PalmControl import PalmControlListener  # For palm-tilt based control
from FingerControl import FingerControlListener  # For finger-pointing control
from MotionControl import MotionControlListener  # For motion control
from DynamicControl import DynamicControlListener  # For dynamic controls


def show_help():
    print "----------------------------------PyLeapMouse----------------------------------"
    print "Use --finger (or blank) for pointer finger control, and --palm for palm control."
    print "Set smooth aggressiveness (# samples) with \"--smooth-aggressiveness [# samples]\""
    print "Set smooth falloff with \"--smooth-falloff [% per sample]\""
    print "Read README.md for even more info.\n"


class MouseMode(object):
    MODE_DYNAMIC = 1
    MODE_FINGER = 2
    MODE_MOTION = 3
    MODE_PALM = 4

    mode = MODE_DYNAMIC
    aggressiveness = 8
    falloff = 1.3

    def __init__(self):
        super(MouseMode, self).__init__()

    def set_mode(self, mode):
        self.mode = mode

    def get_mode(self):
        return self.mode

    def set_aggressiveness(self, aggressiveness):
        self.aggressiveness = aggressiveness

    def get_aggressiveness(self):
        return self.aggressiveness

    def set_falloff(self, falloff):
        self.falloff = falloff

    def get_falloff(self):
        return self.falloff

    def is_dynamic(self):
        return self.get_mode() == self.MODE_DYNAMIC

    def is_finger(self):
        return self.get_mode() == self.MODE_FINGER

    def is_motion(self):
        return self.get_mode() == self.MODE_MOTION

    def is_palm(self):
        return self.get_mode() == self.MODE_PALM


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

    # Introductions
    print "----------------------------------PyLeapMouse----------------------------------"
    print "Use --finger (or blank) for pointer finger control, and --palm for palm control."
    print "Use -h or --help for more info.\n"

    # Get a Leap controller
    controller = Leap.Controller()
    controller.set_policy_flags(Leap.Controller.POLICY_BACKGROUND_FRAMES)

    # Input loop
    while True:
        if listener is not None:
            # Remove previous listener
            controller.remove_listener(listener)
        # Define the listener object which controls the mouse
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

        print "Adding Listener."
        controller.add_listener(listener)  # Attach the listener

        # Keep this process running until Enter is pressed
        print "Press Enter to quit..."
        sys.stdin.readline()

    if listener is not None:
        # Remove the listener when done
        controller.remove_listener(listener)


main()
