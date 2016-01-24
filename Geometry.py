# William Yager
# Leap Python mouse controller POC


import math
from leap import Leap


def to_vector(leap_vector):
    return Vector(leap_vector.x, leap_vector.y, leap_vector.z)


def angle_between_vectors(vector1, vector2):
    # cos(theta)=dot product / (|a|*|b|)
    top = vector1 * vector2  # * is dot product
    bottom = vector1.norm() * vector2.norm()
    angle = math.acos(top / bottom)
    return angle  # In radians


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


def angles_to_velocity(roll, pitch):  # Angles are in radians
    x_movement = 5.0 * math.copysign((4.0 * math.sin(roll) + 2.0 * roll) * math.sin(roll), roll)
    y_movement = 5.0 * math.copysign((4.0 * math.sin(pitch) + 2.0 * pitch) * math.sin(pitch), pitch)
    return x_movement, y_movement


class Vector(object):
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def __add__(self, other):
        return Vector(self.x + other.x, self.y + other.y, self.z + other.z)

    def __sub__(self, other):
        return Vector(self.x - other.x, self.y - other.y, self.z - other.z)

    def __mul__(self, other):  # The * operator is dot product
        return self.dot(other)

    def dot(self, other):
        return self.x * other.x + self.y * other.y + self.z * other.z

    def __pow__(self, other):  # The ** operator allows us to multiply a vector by a scalar
        return self.scalar_mult(other)

    def scalar_mult(self, other):
        return Vector(self.x * other, self.y * other, self.z * other)

    def cross(self, other):
        x = self.y * other.z - other.y * self.z
        y = -(self.x * other.z - other.x * self.z)
        z = self.x * other.y - other.x * self.y
        return Vector(x, y, z)

    def __mod__(self, other):  # The % operator is cross product
        return self.cross(other)

    def norm(self):  # Length of self
        return math.sqrt(1.0 * self.dot(self))

    def distance(self, other):
        return (self - other).norm()  # Find difference and then the length of it

    def unit_vector(self):
        magnitude = self.norm()
        return Vector(1.0 * self.x / magnitude, 1.0 * self.y / magnitude, 1.0 * self.z / magnitude)

    def to_leap(self):
        return Leap.Vector(self.x, self.y, self.z)

    def pitch(self):
        return math.atan(1.0 * self.z / self.y)

    def roll(self):
        return math.atan(1.0 * self.x / self.y)

    def yaw(self):
        return math.atan(1.0 * self.x / self.z)


class Segment(object):
    def __init__(self, point1, point2):
        self.point1 = point1
        self.point2 = point2

    # Shortest distance code based off of http://geomalgorithms.com/a07-_distance.html
    def min_distance_infinite(self, other):  # Return shortest distance between two lines
        u = self.point2 - self.point1
        v = other.point2 - other.point1
        w = self.point1 - other.point1
        a = u * u
        b = u * v
        c = v * v
        d = u * w
        e = v * w
        dd = a * c - b * b
        basically_zero = .000000001
        if dd < basically_zero:
            sc = 0.0
            if b > c:
                tc = d / b
            else:
                tc = e / c
        else:
            sc = (b * e - c * d) / dd
            tc = (a * e - b * d) / dd
        dp = w + u ** sc - v ** tc
        return dp.norm()

    def min_distance_finite(self, other):  # Return shortest distance between two segments
        u = self.point2 - self.point1
        v = other.point2 - other.point1
        w = self.point1 - other.point1
        a = u * u  # * here is cross product
        b = u * v
        c = v * v
        d = u * w
        e = v * w
        dd = a * c - b * b
        sdd = dd
        tdd = dd
        basically_zero = .000000001
        if dd < basically_zero:
            snn = 0.0
            sdd = 1.0
            tnn = e
            tdd = c
        else:
            snn = (b * e - c * d)
            tnn = (a * e - b * d)
            if snn < 0.0:
                snn = 0.0
                tnn = e
                tdd = c
            elif snn > sdd:
                snn = sdd
                tnn = e + b
                tdd = c
        if tnn < 0.0:
            tnn = 0.0
            if -d < 0.0:
                snn = 0.0
            elif -d > a:
                snn = sdd
            else:
                snn = -d
                sdd = a
        elif tnn > tdd:
            tnn = tdd
            if (-d + b) < 0.0:
                snn = 0
            elif (-d + b) > a:
                snn = sdd
            else:
                snn = (-d + b)
                sdd = a
        if abs(snn) < basically_zero:
            sc = 0
        else:
            sc = snn / sdd
        if abs(tnn) < basically_zero:
            tc = 0.0
        else:
            tc = tnn / tdd
        dP = w + u ** sc - v ** tc  # I'm pretty sure dP is the actual vector linking the lines
        return dP.norm()


class Line(Segment):
    def __init__(self, point1, direction_vector, point2):
        super(Line, self).__init__(point1, point2)
        self.point1 = point1
        self.direction = direction_vector.unit_vector()
        self.point2 = point1 + self.direction
