class Object:
    def __init__(self, mass, pos, angle, speed, radius):
        self.mass = mass
        self.pos = pos
        self.angle = angle
        self.speed = speed
        self.radius = radius


class Field:
    def __init__(self, decay):
        self.decay = decay