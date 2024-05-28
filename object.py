class Object:
    def __init__(self, mass, radius, decay, restitution):
        self.mass = mass
        self.radius = radius
        self.decay = decay
        self.restitution = restitution

    def map(self):
        return {
            "mass": self.mass,
            "radius": self.radius,
            "decay": self.decay,
            "restitution": self.restitution
        }