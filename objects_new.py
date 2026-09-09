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
        self.image = None
        self.image_rect = None
        self.update_image()
        self.image_index = 0

        self.collision_rect = pygame.Rect(self.pos[0], self.pos[1], self.size, self.size)

        self.direction = 'S'
        self.moving = False
        self.walking_slower_down = 0

        self.shadow_image = None
        self.shadow_pos = None
        self.s_direction = 0
        self.s_angle = 315
        self.s_length = 1
        self.s_end_pos_rect = None

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

    def increment_walking_slower_down(self):
        self.walking_slower_down += 1
        self.walking_slower_down %= 7
        if self.walking_slower_down == 0:
            self.image_index += 1
            self.image_index %= 7

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
        if self.moving:
            self.increment_walking_slower_down()
        else:
            self.image_index = 0
        self.image = pygame.image.load(self.images[self.direction][self.image_index]).convert_alpha()
        ratio = self.size / self.image.get_width()
        self.image = pygame.transform.scale(self.image, (self.size, self.image.get_height() * ratio))
        self.image_rect = self.image.get_rect()

    def draw_player(self, screen):
        self.update_image()
        self.update_shadow_image()
        self.update_s_end_pos()
        screen.blit(self.image, self.image_rect)
        screen.blit(self.shadow_image, self.shadow_pos)

    def make_shadow_image(self):
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

    def update_shadow_image(self):

        move_vector = pygame.Vector2(self.s_length * self.image.get_height(), 0).rotate(self.s_angle % 360)
        self.shadow_image = self.make_shadow_image()
        self.shadow_image = pygame.transform.smoothscale(self.shadow_image, (self.size, abs(move_vector[1])))

        self.shadow_image = self.shear_image(move_vector[0])

        if 270 <= self.s_angle <= 360 or 0 <= self.s_angle <= 90:
            corner_x = self.pos[0] - self.size / 2
        else:
            corner_x = self.pos[0] - self.size / 2 + move_vector[0]

        if 0 <= self.s_angle <= 180:
            corner_y = self.pos[1] + self.image.get_height() / 2
            image = pygame.transform.flip(self.shadow_image, False, True)
        else:
            corner_y = self.pos[1] + self.image.get_height() / 2 + move_vector[1]

        self.shadow_pos = (corner_x, corner_y)

    def update_s_end_pos(self):
        offset = pygame.Vector2(self.s_length * self.size, 0)
        rotated_offset = offset.rotate(self.s_angle)
        pos = pygame.Vector2(self.pos) + rotated_offset
        self.s_end_pos_rect = pygame.Rect(pos[0], pos[1], self.size, self.size)
















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