import pygame

class GameObject:
    def __init__(self, controller, name, pos, solid, size, transparent):
        self.controller = controller
        self.name = name
        self.pos = pos
        self.size = size
        self.solid = solid
        self.transparent = transparent

    def __repr__(self):
        return f'GameObject(name: {self.name}, pos: {self.pos}, size: {self.size}, solid: {self.solid}, transparent: {self.transparent})'

    def get_name(self):
        return self.name
    def get_pos(self):
        return self.pos
    def get_size(self):
        return self.size
    def get_solid(self):
        return self.solid
    def get_transparent(self):
        return self.transparent

class Player(GameObject):
    def __init__(self, controller, name, pos, solid, size, transparent, speed):
        GameObject.__init__(self, controller, name, pos, solid, size, transparent)
        self.solid = True
        self.transparent = False
        self.speed = speed
        self.direction = 0
        self.s_angle = 0
        self.s_length = 1 #this should be an integer n s.t. the actual shadow length is n*player.size

    def __repr__(self):
        return f'Player(name: {self.name}, pos: {self.pos}, size: {self.size}, solid: {self.solid}, transparent: {self.transparent}, speed: {self.speed}, s_angle: {self.s_angle}, s_length: {self.s_length})'

    def get_speed(self):
        return self.speed
    def get_s_angle(self):
        return self.s_angle
    def get_s_length(self):
        return self.s_length

    def get_s_end_pos(self):
        offset = pygame.Vector2(self.s_length * self.size, 0)
        rotated_offset = offset.rotate(self.s_angle)
        return pygame.Vector2(self.pos) + rotated_offset

    def find_next_location(self, key):
        if key == 'W':
            return self.pos[0], self.pos[1] - self.speed
        elif key == 'A':
            return self.pos[0] - self.speed, self.pos[1]
        elif key == 'S':
            return self.pos[0], self.pos[1] + self.speed
        elif key == 'D':
            return self.pos[0] + self.speed, self.pos[1]
        return None

    def move(self, key):
        self.pos = self.find_next_location(key)

    def move_to_pos(self, pos):
        self.pos = pos

    def s_rotate(self, key):
        if key == 'P':
            self.s_angle += 1
        elif key == 'O':
            self.s_angle -= 1

    def s_lengthen(self, key):
        if key == 'K':
            self.s_length -= 1
            if self.s_length <= 0:
                self.s_length = 0
        elif key == 'L':
            self.s_length += 1
            if self.s_length >= 10:
                self.s_length = 10

    def s_rotate_by(self, degrees):
        self.s_angle += degrees
        self.s_angle %= 360

    def s_snap_angle(self):
        self.s_angle = round(self.s_angle / 45) * 45
        self.s_angle %= 360

class Key(GameObject):
    def __init__(self, controller, name, pos, solid, size, transparent, colour):
        GameObject.__init__(self, controller, name, pos, solid, size, transparent)
        self.solid = False
        self.transparent = True
        self.colour = colour
        self.key_found = False

        def get_key_found():
            return self.key_found
        def get_colour():
            return self.colour

class Door(Key):
    def __init__(self, controller, name, pos, solid, size, transparent, colour):
        Key.__init__(self, controller, name, pos, solid, size, transparent, colour)
        self.solid = True
        self.transparent = False

        def open_door():
            self.solid = False
            self.transparent = True