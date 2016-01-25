class MouseMode(object):
    MODE_DYNAMIC = 1
    MODE_FINGER = 2
    MODE_MOTION = 3
    MODE_PALM = 4

    mode = MODE_DYNAMIC
    aggressiveness = 8
    falloff = 1.3
    scroll_direction = -1

    def __init__(self):
        super(MouseMode, self).__init__()

    def set_mode(self, mode):
        self.mode = mode

    def get_mode(self):
        return self.mode

    def get_mode_string(self):
        if self.mode == 1:
            return 'DYNAMIC'
        elif self.mode == 2:
            return 'FINGER'
        elif self.mode == 3:
            return 'MOTION'
        elif self.mode == 4:
            return 'PALM'
        return 'NONE'

    def set_aggressiveness(self, aggressiveness):
        # print "Aggression factor set to: {}".format(aggressiveness)
        self.aggressiveness = aggressiveness

    def get_aggressiveness(self):
        return self.aggressiveness

    def set_falloff(self, falloff):
        # print "Falloff set to: {}".format(falloff)
        self.falloff = falloff

    def get_falloff(self):
        return self.falloff

    def is_dynamic(self, listener=None):
        if listener is not None:
            return listener.__class__.__name__ is 'DynamicControlListener'
        return self.get_mode() == self.MODE_DYNAMIC

    def is_finger(self, listener=None):
        if listener is not None:
            return listener.__class__.__name__ is 'FingerControlListener'
        return self.get_mode() == self.MODE_FINGER

    def is_motion(self, listener=None):
        if listener is not None:
            return listener.__class__.__name__ is 'MotionControlListener'
        return self.get_mode() == self.MODE_MOTION

    def is_palm(self, listener=None):
        if listener is not None:
            return listener.__class__.__name__ is 'PalmControlListener'
        return self.get_mode() == self.MODE_PALM

    def is_none(self, listener=None):
        if listener is None:
            return True
        return self.get_mode() is None
