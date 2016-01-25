# William Yager
# Leap Python mouse controller POC
import sys
import UserInterface as UI
from MouseMode import MouseMode
from leap import Leap, Mouse
from PalmControl import PalmControlListener  # For palm-tilt based control
from FingerControl import FingerControlListener  # For finger-pointing control
from MotionControl import MotionControlListener  # For motion control
from DynamicControl import DynamicControlListener  # For dynamic controls

listener = None
controller = None
changed = True
running = True


def main():
    if "-h" in sys.argv or "--help" in sys.argv:
        UI.show_help()
        return

    # Defaults
    global listener, controller, changed
    mode = MouseMode()

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
        if "--width" in arg:
            UI.console_width = int(sys.argv[i + 1])

    # Display the initial help content
    UI.console_help()

    # Get a Leap controller
    controller = Leap.Controller()
    controller.set_policy_flags(Leap.Controller.POLICY_BACKGROUND_FRAMES)

    # Input loop
    while running:
        # Define the listener object which controls the mouse
        if changed:
            print UI.spacer(wall='')
            print UI.header(mode.get_mode_string())
            try:
                if mode.is_dynamic():  # Dynamic pointer mode
                    listener = DynamicControlListener(
                            Mouse,
                            aggressiveness=mode.get_aggressiveness(),
                            falloff=mode.get_falloff()
                    )
                elif mode.is_finger():  # Finger pointer mode
                    listener = FingerControlListener(
                            Mouse,
                            aggressiveness=mode.get_aggressiveness(),
                            falloff=mode.get_falloff()
                    )
                elif mode.is_palm():  # Palm control mode
                    listener = PalmControlListener(Mouse)
                elif mode.is_motion():  # Motion control mode
                    listener = MotionControlListener(Mouse)
                # elif mode.is_none():  # Mode is not set
                #     break
            except Exception as e:
                print UI.build_error('{}'.format(e.message))

            # print UI.build_status('Adding listener')
            if listener is not None:
                controller.add_listener(listener)  # Attach the listener
            changed = False

        # Display options menu and await input
        mode = prompt(mode)

    if listener is not None:
        # Remove the listener when done
        controller.remove_listener(listener)
        print UI.footer(mode.get_mode_string())
        print UI.spacer(wall='')


def set_mode(mode, value):
    global listener, controller, changed
    if listener is not None and \
            (listener.__class__ is not DynamicControlListener.__class__ and mode.is_dynamic()) or \
            (listener.__class__ is not FingerControlListener.__class__ and mode.is_finger()) or \
            (listener.__class__ is not MotionControlListener.__class__ and mode.is_motion()) or \
            (listener.__class__ is not PalmControlListener.__class__ and mode.is_palm()):
        changed = True
        if listener is not None:
            # Remove previous listener
            controller.remove_listener(listener)
            listener = None
    elif listener is None and mode.mode is None and value is not None:
        changed = True
    if changed:
        print UI.footer(mode.get_mode_string())
        print UI.spacer(wall='')
    mode.set_mode(value)
    return mode


def prompt(mode):
    # Keep this process running until Enter is pressed
    # print UI.BAR_WHITE + UI.GT_WHITE + ' '
    global running
    choice = UI.get_input()  # sys.stdin.readline()
    if "dynamic" in choice:
        mode = set_mode(mode, MouseMode.MODE_DYNAMIC)
    if "finger" in choice:
        mode = set_mode(mode, MouseMode.MODE_FINGER)
    if "motion" in choice:
        mode = set_mode(mode, MouseMode.MODE_MOTION)
    if "palm" in choice:
        mode = set_mode(mode, MouseMode.MODE_PALM)
    if "quit" in choice or "exit" in choice:
        running = False
    if "stop" in choice:
        mode = set_mode(mode, None)
    if "info" in choice:
        UI.show_info(mode)
    if "falloff" in choice:
        key, value = choice.split(' ', 1)
        try:
            mode.set_falloff(float(value))
            print UI.build_status('Updated falloff to', value)
        except Exception as e:
            print UI.build_error('{}'.format(e.message))
    if "aggression" in choice:
        key, value = choice.split(' ', 1)
        try:
            mode.set_aggressiveness(int(value))
            print UI.build_status('Updated aggression to', value)
        except Exception as e:
            print UI.build_error('{}'.format(e.message))
    if "width" in choice:
        key, value = choice.split(' ', 1)
        UI.console_width = int(value)
        print UI.build_status('Updated console width to', value)
    if "help" in choice:
        if " " in choice:
            key, value = choice.split(' ', 1)
            UI.console_help(control=value)
        else:
            UI.console_help(wall=UI.clr.w('|'))
    return mode

main()
