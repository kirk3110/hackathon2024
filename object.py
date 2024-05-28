class Object:
    def __init__(self, mass, radius):
        self.mass = mass
        self.radius = radius

    def map(self):
        return {
            "mass": self.mass,
            "radius": self.radius
        }