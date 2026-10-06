from game_objects_new import GameObject, Player, Key
import pygame

class Game:
    def __init__(self, objects, keys, player):
        self.player = (Player(self, player[0], player[1], player[2], player[3], player[4]))
        self.backgrounds = []
        self.keys = []
        if objects is not None:
            for obj in objects:
                self.add_background_object(obj)
        if keys is not None:
            for key in keys:
                self.add_key(key)

    def set_up(self):
        pass

    def add_background_object(self, obj):
        self.backgrounds.append(GameObject(self, obj[0], obj[1], obj[2], obj[3], obj[4], obj[5], obj[6], obj[7]))
        #controller, name, pos, size, solid, transparent, interactable, image, colour

    def add_key(self, key):
        self.keys.append(Key(self, key[0], key[1], key[2], key[3], key[4], key[5], key[6], key[7]))
        #self, controller, name, pos, size, image, colour, door_pos, door_size, door_images'

    def get_background_objects(self):
        return self.backgrounds

    def get_keys(self):
        return self.keys

    def check_collisions(self, new_pos):
        new_rect = pygame.Rect(new_pos[0], new_pos[1] - self.player.get_size(), self.player.get_size(), self.player.get_size())
        for thing in self.backgrounds:
            if pygame.Rect.colliderect(new_rect, thing.get_collision_rect()):
                if thing.get_solid():
                    return True
        for door in self.keys:
            if pygame.Rect.colliderect(new_rect, door.door.get_collision_rect()):
                if door.door.get_solid():
                    return True
        return False

    def scan_radius(self):
        possibilities = []
        for thing in self.backgrounds:
            if (((thing.get_pos()[0] + thing.get_size() / 2) - (self.player.get_pos()[0] + self.player.get_size() / 2))**2 +
                    ((thing.get_pos()[1] + thing.get_size() / 2) - (self.player.get_pos()[1] + self.player.get_size() / 2))**2 <= (thing.get_interaction_radius())**2):
                possibilities.append(thing)
                if thing.get_interactable():
                    possibilities.append(thing)
        for key in self.keys:
            if (((key.get_pos()[0] + key.get_size() / 2) - (self.player.get_pos()[0] + self.player.get_size() / 2)) ** 2 +
                    ((key.get_pos()[1] + key.get_size() / 2) - (self.player.get_pos()[1] + self.player.get_size() / 2)) ** 2 <= (key.get_interaction_radius()) ** 2):
                possibilities.append(key)
            if (((key.door.get_pos()[0] + key.door.get_size() / 2) - (self.player.get_pos()[0] + self.player.get_size() / 2)) ** 2 +
                    ((key.door.get_pos()[1] + key.door.get_size() / 2) - (self.player.get_pos()[1] + self.player.get_size() / 2)) ** 2 <= (key.door.get_interaction_radius()) ** 2):
                possibilities.append(key.door)

        if len(possibilities) == 0:
            return None
        else:
            print(possibilities)
            return possibilities

    def move_character_by_key(self, key):
        move = False
        new_pos = self.player.find_next_location(key)
        if not self.check_collisions(new_pos):
            self.player.move(key)
            move = True
        return move

    def move_character_by_pos(self, pos):
        move = False
        if not self.check_collisions(pos):
            self.player.move_to_pos(pos)
            move = True
        return move

    def make_swap(self):
        if not self.check_collisions((self.player.get_s_end_pos()[0], self.player.get_s_end_pos()[1] + self.player.get_size())):
            self.move_character_by_pos((self.player.get_s_end_pos()[0], self.player.get_s_end_pos()[1] + self.player.get_size()))
            self.player.s_rotate_by(180)
            return True
        else:
            return False