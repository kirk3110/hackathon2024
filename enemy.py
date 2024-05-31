from object import Object


class Enemy:
    def __init__(self, pos_x, pos_y, vel_x, vel_y, obj: Object):
        self.obj = obj
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.vel_x = vel_x
        self.vel_y = vel_y
