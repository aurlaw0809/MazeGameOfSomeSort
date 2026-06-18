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
    def __init__(self, controller, name, pos, solid, size, transparent, speed, s_angle, s_length):
        GameObject.__init__(self, controller, name, pos, solid, size, transparent)
        self.speed = speed
        self.s_angle = s_angle
        self.s_length = s_length #this should be an integer n s.t. the actual shadow length is n*player.size

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

class Key(GameObject):
    def __init__(self, controller, name, pos, solid, size, transparent, colour):
        GameObject.__init__(self, controller, name, pos, solid, size, transparent)
        self.colour = colour
        self.key_found = False

        def get_key_found():
            return self.key_found

class Door(Key):
    def __init__(self, controller, name, pos, solid, size, transparent, colour):
        Key.__init__(self, controller, name, pos, solid, size, transparent, colour)