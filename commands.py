
from leap import Leap, CircleGesture, KeyTapGesture, ScreenTapGesture, SwipeGesture

class ScreentapCommand:
    def __init__(self):
        self.name = "screentap"
        # The name of the command in the config file

    # Return true if the command is applicable
    @staticmethod
    def applicable(frame):
        return frame.gestures()[0].type == Leap.Gesture.TYPE_SCREEN_TAP


class KeytapCommand:
    def __init__(self):
        self.name = "keytap"  # The name of the command in the config file

    # Return true if the command is applicable
    @staticmethod
    def applicable(frame):
        return frame.gestures()[0].type == Leap.Gesture.TYPE_KEY_TAP


class SwiperightCommand:
    def __init__(self):
        self.name = "swiperight"  # The name of the command in the config file

    # Return true if the command is applicable
    @staticmethod
    def applicable(frame):
        swipe = SwipeGesture(frame.gestures()[0])
        return (swipe.state == Leap.Gesture.STATE_STOP
                and swipe.type == Leap.Gesture.TYPE_SWIPE
                and swipe.direction[0] < 0)


class SwipeleftCommand:
    def __init__(self):
        self.name = "swipeleft"  # The name of the command in the config file

    # Return true if the command is applicable
    @staticmethod
    def applicable(frame):
        swipe = SwipeGesture(frame.gestures()[0])
        return (swipe.state == Leap.Gesture.STATE_STOP
                and swipe.type == Leap.Gesture.TYPE_SWIPE
                and swipe.direction[0] > 0)


class ClockwiseCommand:
    def __init__(self):
        self.name = "clockwise"  # The name of the command in the config file

    # Return true if the command is applicable
    @staticmethod
    def applicable(frame):
        circle = CircleGesture(frame.gestures()[0])
        return (circle.state == Leap.Gesture.STATE_STOP and
                circle.type == Leap.Gesture.TYPE_CIRCLE and
                circle.pointable.direction.angle_to(circle.normal) <= Leap.PI / 4)


class CounterclockwiseCommand:
    def __init__(self):
        self.name = "counterclockwise"  # The name of the command in the config file

    # Return true if the command is applicable
    @staticmethod
    def applicable(frame):
        circle = CircleGesture(frame.gestures()[0])
        return (circle.state == Leap.Gesture.STATE_STOP and
                circle.type == Leap.Gesture.TYPE_CIRCLE and
                circle.pointable.direction.angle_to(circle.normal) > Leap.PI / 4)
