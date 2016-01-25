# William Yager
# Leap Python mouse controller POC
# This file is for pointer-finger-based control (--finger and default)


import math
import UserInterface as UI
import Geometry
from leap import Leap, Mouse
from MiscFunctions import *

# print 'Width: {}, Height: {}'.format(Mouse.GetDisplayWidth(), Mouse.GetDisplayHeight())


# The Listener that we attach to the controller. This listener is for pointer finger movement
class DynamicControlListener(Leap.Listener):
    # Last Touch, Dynamic Count
    lt, fc = 0, 0
    # Dynamic Positions
    fstate = {'INDEX': False}

    def __init__(self, mouse, aggressiveness=8, falloff=1.3):
        # Initialize like a normal listener
        super(DynamicControlListener, self).__init__()
        # Initialize a bunch of stuff specific to this implementation
        self.screen = None
        self.screen_resolution = (Mouse.GetDisplayWidth(), Mouse.GetDisplayHeight())
        # The cursor object that lets us control mice cross-platform
        self.cursor = mouse.absolute_cursor()
        # Keeps the cursor from fidgeting
        self.mouse_position_smoother = MousePositionSmoother(aggressiveness, falloff)
        # A signal debouncer that ensures a reliable, non-jumpy click
        self.mouse_button_debouncer = Debouncer(5)
        # This holds the ID of the most recently used pointing finger, to prevent annoying switching
        self.most_recent_pointer_finger_id = None

    def on_init(self, controller):
        print UI.build_status(self.__class__.__name__, " Initialized")

    def on_connect(self, controller):
        print UI.build_status(self.__class__.__name__, " Connected")
        print UI.spacer(wall=UI.clr.w('|'))
        print UI.spacer(wall=UI.clr.w('|'))
        controller.enable_gesture(Leap.Gesture.TYPE_KEY_TAP)

    def on_disconnect(self, controller):
        print UI.build_status(self.__class__.__name__, " Disconnected")

    def on_exit(self, controller):
        print UI.build_status(self.__class__.__name__, " Exited")

    @staticmethod
    def finger_type(finger):
        if finger.type == Leap.Finger.TYPE_THUMB:
            return 'THUMB'
        elif finger.type == Leap.Finger.TYPE_INDEX:
            return 'INDEX'
        elif finger.type == Leap.Finger.TYPE_MIDDLE:
            return 'MIDDLE'
        elif finger.type == Leap.Finger.TYPE_RING:
            return 'RING'
        elif finger.type == Leap.Finger.TYPE_PINKY:
            return 'PINKY'
        return 'UNKNOWN'

    @staticmethod
    def touch_zone(finger):
        if finger.touch_zone == Leap.Finger.ZONE_NONE:
            return 'NONE'
        elif finger.touch_zone == Leap.Finger.ZONE_HOVERING:
            return 'HOVERING'
        elif finger.touch_zone == Leap.Finger.ZONE_TOUCHING:
            return 'TOUCHING'
        return 'UNKNOWN'

    def on_frame(self, controller):
        frame = controller.frame()  # Grab the latest 3D data
        if not frame.hands.is_empty:  # Ensure a hand is available
            if len(frame.hands) < 2:  # Single hand
                self.do_mouse_stuff(frame.hands[0])
            # else:  # 2+ hands
        finger_count = len(frame.fingers)
        if finger_count != self.fc:
            self.fc = finger_count
        if finger_count < 1:
            self.fstate = {'INDEX': False}
            return
        finger = frame.fingers.frontmost
        for f in frame.fingers:
            if f.type == Leap.Finger.TYPE_INDEX:
                finger = f
        stabilized_position = finger.stabilized_tip_position
        interaction_box = frame.interaction_box
        normalized_position = interaction_box.normalize_point(stabilized_position)
        f_state = '{}-{}'.format(self.finger_type(finger), self.touch_zone(finger))
        new_x = normalized_position.x * self.screen_resolution[0]
        new_y = self.screen_resolution[1] - normalized_position.y * self.screen_resolution[1]
        self.cursor.move(new_x, new_y)
        if finger.id in self.fstate.keys() \
                and self.fstate[finger.id] != f_state \
                or finger.id not in self.fstate.keys():
            self.fstate[finger.id] = '{}'.format(f_state)
            # if self.touch_zone(finger) == 'NONE':
            #     self.cursor.set_left_button_pressed(False)
            # elif finger.is_extended:
            #     self.fstate['INDEX'] = False if self.fstate['INDEX'] else True
            #     self.cursor.set_left_button_pressed(self.fstate['INDEX'])
        UI.erase_line_up(2)
        print UI.build_status('Position', '{} x {}'.format(new_x, new_y))
        print UI.build_status('Finger', '{}, {}, {}'.format(finger.id, self.finger_type(finger), self.touch_zone(finger)))

            # if finger.touch_zone > 0:
            #     if finger.touch_zone == 1:
            #         self.cursor.set_left_button_pressed(False)
            #         if finger_count < 5:
            #             self.cursor.move(normalized_position.x * self.screen_resolution[0],
            #             self.screen_resolution[1] - normalized_position.y * self.screen_resolution[1])
            #         elif finger_count == 5:
            #             finger_velocity = finger.tip_velocity
            #             x_scroll = self.velocity_to_scroll_amount(finger_velocity.x)
            #             y_scroll = self.velocity_to_scroll_amount(finger_velocity.y)
            #             self.cursor.scroll(x_scroll, y_scroll)
            #         else:
            #             print "Dynamic count: %s" % finger_count
            #     elif finger.touch_zone == 2:
            #         if finger_count == 1:
            #             self.cursor.set_left_button_pressed(True)
            #         elif finger_count == 2:
            #             self.cursor.set_left_button_pressed(True)
            #             self.cursor.move(normalized_position.x * self.screen_resolution[0],
            #             self.screen_resolution[1] - normalized_position.y * self.screen_resolution[1])
            # if(finger.touch_distance > -0.3 and finger.touch_zone != Leap.Pointable.ZONE_NONE):
            # self.cursor.set_left_button_pressed(False)
            # self.cursor.move(normalized_position.x * self.screen_resolution[0],
            # self.screen_resolution[1] - normalized_position.y * self.screen_resolution[1])
            # elif(finger.touch_distance <= -0.4):
            # self.cursor.set_left_button_pressed(True)
            #    print finger.touch_distance

    def do_scroll_stuff(self, hand):  # Take a hand and use it as a scroller
        fingers = hand.fingers  # The list of fingers on said hand
        if not fingers.is_empty:  # Make sure we have some fingers to work with
            sorted_fingers = sort_fingers_by_distance_from_screen(fingers)  # Prioritize fingers by distance from screen
            finger_velocity = sorted_fingers[0].tip_velocity  # Get the velocity of the forward-most finger
            x_scroll = self.velocity_to_scroll_amount(finger_velocity.x)
            y_scroll = self.velocity_to_scroll_amount(finger_velocity.y)
            self.cursor.scroll(x_scroll, y_scroll)

    @staticmethod
    def velocity_to_scroll_amount(velocity):  # Converts a finger velocity to a scroll velocity
        # The following algorithm was designed to reflect what I think is a comfortable
        # Scrolling behavior.
        vel = velocity  # Save to a shorter variable
        vel += math.copysign(300, vel)  # Add/subtract 300 to velocity
        vel /= 150
        vel **= 3  # Cube vel
        vel /= 8
        vel *= -1  # Negate direction, depending on how you like to scroll
        return vel

    def do_mouse_stuff(self, hand):
        hpn = hand.palm_normal
        d = Geometry.Vector(hpn.x, hpn.y, hpn.z)
        mouse_velocity = Geometry.angles_to_velocity(d.roll(), d.pitch())
        self.cursor.move(mouse_velocity[0], mouse_velocity[1])
        # # Take a hand and use it as a mouse
        # fingers = hand.fingers  # The list of fingers on said hand
        # if not fingers.is_empty:  # Make sure we have some fingers to work with
        #     pointer_finger = self.select_pointer_finger(fingers)  # Determine which finger to use
        #
        #     try:
        #         intersection = self.screen.intersect(pointer_finger,
        #                                              True)  # Where the finger projection intersects with the screen
        #         if not math.isnan(intersection.x) and not math.isnan(
        #                 intersection.y):  # If the finger intersects with the screen
        #             x_coord = intersection.x * self.screen_resolution[0]  # x pixel of intersection
        #             y_coord = (1.0 - intersection.y) * self.screen_resolution[1]  # y pixel of intersection
        #             x_coord, y_coord = self.mouse_position_smoother.update((x_coord, y_coord))  # Smooth movement
        #             self.cursor.move(x_coord, y_coord)  # Move the cursor
        #             if has_thumb(hand):  # We've found a thumb!
        #                 # We have detected a possible click. The debouncer ensures that we don't have click jitter
        #                 self.mouse_button_debouncer.signal(True)
        #             else:
        #                 self.mouse_button_debouncer.signal(False)  # Same idea as above (but opposite)
        #
        #             # We need to push/unpush the cursor's button
        #             if self.cursor.left_button_pressed != self.mouse_button_debouncer.state:
        #                 self.cursor.set_left_button_pressed(
        #                         self.mouse_button_debouncer.state)  # Set the cursor to click/not click
        #     except Exception as e:
        #         print e

    def select_pointer_finger(self, possible_fingers):  # Choose the best pointer finger
        sorted_fingers = sort_fingers_by_distance_from_screen(
                possible_fingers)  # Prioritize fingers by distance from screen
        if self.most_recent_pointer_finger_id is not None:  # If we have a previous pointer finger in memory
            for finger in sorted_fingers:  # Look at all the fingers
                # The previously used pointer finger is still in frame
                if finger.id == self.most_recent_pointer_finger_id:
                    return finger  # Keep using it
        # If we got this far, it means we don't have any previous pointer fingers
        # OR we didn't find the most recently used pointer finger in the frame
        self.most_recent_pointer_finger_id = sorted_fingers[0].id  # This is the new pointer finger
        return sorted_fingers[0]
