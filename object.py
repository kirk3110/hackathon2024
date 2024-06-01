import numpy as np
class Object:
    def __init__(self, mass, radius, decay, restitution, rps):
        self.mass = mass
        self.radius = radius
        self.decay = decay
        self.restitution = restitution
        self.rps = rps

    def map(self):
        return {
            "mass": self.mass,
            "radius": self.radius,
            "decay": self.decay,
            "restitution": self.restitution,
            "rps": self.rps
        }


class Wall:
    def __init__(self, position, normal_vector):
        self.position = position
        self.normal_vector = normal_vector

    def detect_collision(self, radius, position, velocity):
        return np.dot(self.normal_vector, (position - self.position)) / np.linalg.norm(self.normal_vector) < radius and np.dot(self.normal_vector, velocity) < 0

    def reflect(self, vector):
        return vector - self.normal_vector * 2 * np.dot(self.normal_vector, vector) / np.dot(self.normal_vector, self.normal_vector)
