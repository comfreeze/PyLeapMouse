import sys, os, ConfigParser
import UserInterface as UI
from leap import Leap, ScreentapCommand, SwiperightCommand, SwipeleftCommand, CounterclockwiseCommand, ClockwiseCommand, KeytapCommand


# The Listener that we attach to the controller. This listener is for motion control
class MotionControlListener(Leap.Listener):
    last_command = None
    last_count = 0

    def __init__(self, mouse):
        super(MotionControlListener, self).__init__()  # Initialize like a normal listener

    def on_init(self, controller):
        print UI.build_status(self.__class__.__name__, " Initialized")
        self.read_config()  # Read the config file
        self.init_list_of_commands()  # Initialize the list of recognized commands

    def read_config(self):
        self.config = ConfigParser.ConfigParser()
        self.config.read("./commands.ini")

    def init_list_of_commands(self):
        # Initialize all commands an put it in an array
        self.commands = [
            ScreentapCommand(),
            SwiperightCommand(),
            SwipeleftCommand(),
            CounterclockwiseCommand(),
            ClockwiseCommand(),
            KeytapCommand()
        ]

    def on_connect(self, controller):
        print UI.build_status(self.__class__.__name__, " Connected")
        # Enable all gestures
        controller.enable_gesture(Leap.Gesture.TYPE_CIRCLE)
        controller.enable_gesture(Leap.Gesture.TYPE_KEY_TAP)
        controller.enable_gesture(Leap.Gesture.TYPE_SCREEN_TAP)
        controller.enable_gesture(Leap.Gesture.TYPE_SWIPE)
        UI.stream_updates({'Executing': ' '})

    def on_disconnect(self, controller):
        print UI.build_status(self.__class__.__name__, " Disconnected")

    def on_exit(self, controller):
        print UI.build_status(self.__class__.__name__, " Exited")

    def on_frame(self, controller):
        frame = controller.frame()  # Grab the latest 3D data
        if not frame.hands.is_empty:  # Make sure we have some hands to work with
            for command in self.commands:  # Loop all enabled commands
                if command.applicable(frame):  # If the motion associated to the command is triggered
                    if self.last_command is not command.name:
                        self.last_count = 0
                        self.last_command = command.name
                    else:
                        self.last_count += 1
                    UI.stream_updates({'Executing': '{} x {}'.format(command.name, self.last_count)})
                    self.execute(frame, command.name)  # Execute the command

    def execute(self, frame, command_name):
        number_for_fingers = self.get_fingers_code(frame)  # Get a text correspond to the number of fingers
        if self.config.has_option(command_name, number_for_fingers):  # If the command if found in the config file
            syscmd = self.config.get(command_name, number_for_fingers)  # Prepare the command
            print UI.build_status('Command', syscmd)
            os.system(syscmd)  # Execute the command

    @staticmethod
    def get_fingers_code(frame):
        return "%dfinger" % len(frame.fingers)
