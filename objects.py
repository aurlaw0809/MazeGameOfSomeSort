from pygame import key


class Object:
    def __init__(self, controller, name, pos, solid, size):
        self.controller = controller
        self.name = name
        self.pos = pos
        self.solid = solid
        self.size = size

    def __repr__(self):
        return f'name: {self.name}, pos: {self.pos}, solid: {self.solid}'

    def is_solid(self):
        return self.solid

    def get_size(self):
        return self.size


class Character(Object):
    def __init__(self, controller, name, pos, solid, size, speed, s_length):
        super().__init__(controller, name, pos, solid, size)

        self.speed = speed
        self.s_direction = 0
        self.rotating_clock = False
        self.rotating_aclock = False
        self.s_length = s_length

    def __repr__(self):
        return f'name: {self.name}, pos: {self.pos}, solid: {self.solid}, size: {self.size}, speed: {self.speed}'

    def get_shadow_direction(self):
        return self.s_direction

    def get_shadow_length(self):
        return self.s_length

    def update_shadow_direction(self, angle):
        self.s_direction = (self.s_direction + angle) % 360

    def find_next_location(self, key):
        if key.upper() == 'W':
            return self.pos[0], self.pos[1] + self.speed
        elif key.upper() == 'A':
            return self.pos[0] - self.speed, self.pos[1]
        elif key.upper() == 'S':
            return self.pos[0], self.pos[1] - self.speed
        elif key.upper() == 'D':
            return self.pos[0] + self.speed, self.pos[1]
        return None

    def move(self, key):
        self.pos = self.find_next_location(key)

    def move_by_vector(self, vector):
        self.pos = self.pos[0] + vector.x, self.pos[1] + vector.y


