# William Yager
# Leap Python mouse controller POC
import sys
import colorama as colors
import UserInterface as UI
from MouseMode import MouseMode
from leap import Leap, Mouse
from PalmControl import PalmControlListener  # For palm-tilt based control
from FingerControl import FingerControlListener  # For finger-pointing control
from MotionControl import MotionControlListener  # For motion control
from DynamicControl import DynamicControlListener  # For dynamic controls


def main():
    if "-h" in sys.argv or "--help" in sys.argv:
        UI.show_help()
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
    UI.console_help()

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
            UI.build_error('{}'.format(e.message))

        print "Adding Listener."
        controller.add_listener(listener)  # Attach the listener

        # Display options menu and await input
        mode = prompt(mode)

    if listener is not None:
        # Remove the listener when done
        controller.remove_listener(listener)


def prompt(mode):
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
    if "info" in choice:
        UI.show_info(mode)
    if "falloff" in choice:
        key, value = choice.split(' ', 1)
        mode.set_falloff(float(value))
    if "aggression" in choice:
        key, value = choice.split(' ', 1)
        mode.set_aggressiveness(int(value))
    if "width" in choice:
        key, value = choice.split(' ', 1)
        UI.console_width = int(value)
        print 'Updated console width to: {}'.format(value)
    if "help" in choice:
        if " " in choice:
            key, value = choice.split(' ', 1)
            UI.console_help(control=value)
        else:
            UI.console_help()
    return mode

main()
