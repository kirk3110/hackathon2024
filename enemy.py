import random
from object import Object


class Enemy:
    def __init__(self, level, name, pos_x, pos_y, vel_x, vel_y, obj: Object):
        self.level = level  # レベルが低いほどvelが小さく、Objectのmass, raduis, restitution, rpsが小さくなり、decayは大きくなる
        self.name = name
        self.obj = obj
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.vel_x = vel_x
        self.vel_y = vel_y

    def map(self):
        return {
            "level": self.level,
            "name": self.name,
            "pos_x": self.pos_x,
            "pos_y": self.pos_y,
            "vel_x": self.vel_x,
            "vel_y": self.vel_y,
            "obj": self.obj.map()
        }

    @staticmethod
    def from_map(map_):
        return Enemy(level=map_['level'],
                     name=map_['name'],
                     pos_x=map_['pos_x'],
                     pos_y=map_['pos_y'],
                     vel_x=map_['vel_x'],
                     vel_y=map_['vel_y'],
                     obj=Object(**map_['obj']))

    @staticmethod
    def get_random_enemy(level=None):
        if level is None:
            level = random.randint(1, 5)
        return random.choice([e for e in ENEMY_LIST if e.level == level])


ENEMY_LIST = [
    Enemy(1, "enemy1-1", 0.0, 0.0, 2.0, 1.0, Object(1.0, 1.0, 0.97, 1.0, 15.0)),
    Enemy(1, "enemy1-2", 1.0, 0.0, 1.0, 2.0, Object(0.5, 0.5, 0.98, 1.0, 15.0)),
    Enemy(2, "enemy2-1", 0.0, 1.0, 4.0, 1.0, Object(2.0, 2.0, 0.97, 1.0, 20.0)),
    Enemy(2, "enemy2-2", 1.0, 1.0, 1.0, 4.0, Object(1.0, 1.0, 0.98, 1.0, 20.0)),
    Enemy(3, "enemy3-1", 0.0, 2.0, 5.0, 2.0, Object(3.0, 3.0, 0.98, 1.0, 40.0)),
    Enemy(3, "enemy3-2", 1.0, 2.0, 2.0, 5.0, Object(1.0, 1.0, 0.985, 1.0, 40.0)),
    Enemy(4, "enemy4-1", 0.0, 3.0, 6.0, 2.0, Object(4.0, 4.0, 0.98, 1.0, 50.0)),
    Enemy(4, "enemy4-2", 1.0, 3.0, 2.0, 6.0, Object(2.0, 2.0, 0.985, 1.0, 50.0)),
    Enemy(5, "enemy5-1", 0.0, 4.0, 10.0, 10.0, Object(5.0, 5.0, 0.98, 1.0, 60.0))
]
