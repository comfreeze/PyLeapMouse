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

    def set_aggressiveness(self, aggressiveness):
        print "Aggression factor set to: {}".format(aggressiveness)
        self.aggressiveness = aggressiveness

    def get_aggressiveness(self):
        return self.aggressiveness

    def set_falloff(self, falloff):
        print "Falloff set to: {}".format(falloff)
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
