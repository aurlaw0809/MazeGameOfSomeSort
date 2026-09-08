import pygame

class GameObject:
    def __init__(self, controller, name, pos, size, solid, transparent, interactable):
        self.controller = controller
        self.name = name
        self.pos = pos
        self.size = size
        self.solid = solid
        self.transparent = transparent
        self.interactable = interactable
        self.interaction_radius = 50

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
    def get_interactable(self):
        return self.interactable
    def get_interaction_radius(self):
        return self.interaction_radius





#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#__init__

class Player(GameObject):
    def __init__(self, controller, name, pos, size, speed, images):
        GameObject.__init__(self, controller, name, pos, size, solid = True, transparent = False, interactable = False)

        self.speed = speed
        self.images = images

        self.images = images
        self.image = None
        self.update_image()
        self.image_index = 0

        #TODO stuff with image rects right on

        self.direction = 'S'
        self.moving = False
        self.walking_slower_down = 0

        self.speed = speed

        self.s_direction = 0
        self.s_angle = 315
        self.s_length = 1

        self.rotating_c = False
        self.rotating_ac = False

        self.s_colour = (30, 30, 30, 100)

    def __repr__(self):
        return f'Player(name: {self.name}, pos: {self.pos}, size: {self.size}, solid: {self.solid}, transparent: {self.transparent}, speed: {self.speed}, s_angle: {self.s_angle}, s_length: {self.s_length})'

#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#getters

    def get_speed(self):
        return self.speed

    def get_s_direction(self):
        return self.s_direction
    def get_s_angle(self):
        return self.s_angle
    def get_s_length(self):
        return self.s_length

    def get_rotating_c(self):
        return self.rotating_c
    def get_rotating_ac(self):
        return self.rotating_ac

    def get_direction(self):
        return self.direction
    def get_moving(self):
        return self.moving
    def get_walking_slower_down(self):
        return self.walking_slower_down

    def get_s_end_pos(self):
        offset = pygame.Vector2(self.s_length * self.size, 0)
        rotated_offset = offset.rotate(self.s_angle)
        return pygame.Vector2(self.pos) + rotated_offset

#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#setters

    def set_rotating_c(self, rotating_c):
        self.rotating_c = rotating_c
    def set_rotating_ac(self, rotating_ac):
        self.rotating_ac = rotating_ac

    def set_direction(self, direction):
        self.direction = direction
    def set_moving(self, moving):
        self.moving = moving

    def set_walking_slower_down(self, walking_slower_down):
        self.walking_slower_down = walking_slower_down

#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#finding position and moving player, setters with conditions

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

#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#changing shape of shadow, setters with keys

    def s_rotate(self, key):
        if key == 'P':
            self.s_angle += 1
        elif key == 'O':
            self.s_angle -= 1
        self.s_angle %= 360

    def s_lengthen(self, key):
        if key == 'K':
            self.s_length -= 1
            if self.s_length <= 0:
                self.s_length = 0
        elif key == 'L':
            self.s_length += 1
            if self.s_length >= 6:
                self.s_length = 6

    def s_rotate_by(self, degrees):
        self.s_angle += degrees
        self.s_angle %= 360

#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#updating images

    def update_image(self):
        self.image = self.images[self.direction][self.image_index]


    def draw_player(self, screen):
        screen.blit(self.image, self.pos)


    def shadow_image(self):

        width, height = self.image.get_size()

        new_image = pygame.Surface((width, height), pygame.SRCALPHA)
        for y in range(height):
            for x in range(width):
                pixel = self.image.get_at((x, y))
                if pixel.a == 0:
                    continue

                new_image.set_at((x, y), self.s_colour)

        return new_image

    def shear_image(self, offset):

        width, height = self.image.get_size()

        new_width = width + abs(offset)
        result = pygame.Surface((new_width, height), pygame.SRCALPHA)

        for y in range(height):
            x_offset = int(offset * (height - y) / height)

            if offset < 0:
                x_offset += abs(offset)

            for x in range(width):
                pixel = self.image.get_at((x, y))
                result.set_at((int(x + x_offset), int(y)), pixel)

        return result

    def draw_shadow(self, screen):
        pass
















class Key(GameObject):
    def __init__(self, controller, name, pos, solid, size, transparent, colour):
        GameObject.__init__(self, controller, name, pos, solid, size, transparent)
        self.solid = False
        self.transparent = True
        self.colour = colour
        self.key_found = False
        self.interactable = True

    def get_key_found(self):
        return self.key_found
    def get_colour(self):
        return self.colour

class Door(Key):
    def __init__(self, controller, name, pos, solid, size, transparent, colour):
        Key.__init__(self, controller, name, pos, solid, size, transparent, colour)
        self.solid = True
        self.transparent = False
        self.interactable = True

    def open_door(self):
        self.solid = False
        self.transparent = True