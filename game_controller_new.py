from game_objects_new import GameObject, Player
import pygame

class Game:
    def __init__(self, objects, images, player_images):
        self.player = (Player(self, 'starchy', (0, 0), 50, 10, player_images))
        self.backgrounds = []
        if objects is not None:
            for obj in objects:
                self.add_background_object(obj)

    def set_up(self):
        pass

    def add_background_object(self, obj):
        self.backgrounds.append(GameObject(self, obj[0], obj[1], obj[2], obj[3], obj[4], obj[5], obj[6], obj[7]))
        #controller, name, pos, size, solid, transparent, interactable, image, colour

    def get_background_objects(self):
        return self.backgrounds

    def check_collisions(self, new_pos):
        new_rect = pygame.Rect(new_pos[0], new_pos[1] - self.player.get_size(), self.player.get_size(), self.player.get_size())
        for thing in self.backgrounds:
            if pygame.Rect.colliderect(new_rect, thing.get_collision_rect()):
                if thing.get_solid():
                    return True
                else:
                    return False
        return False

    def scan_radius(self):
        possibilities = []
        for thing in self.backgrounds:
            if (thing.get_pos()[0] + thing.get_size() - self.player.get_pos()[0] - self.player.get_size())**2 + (thing.get_pos()[1] + thing.get_size() - self.player.get_pos()[1] - self.player.get_size())**2 <= (self.player.get_interaction_radius())**2:
                if thing.get_interactable():
                    possibilities.append(thing)
        if len(possibilities) == 0:
            return None
        else:
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