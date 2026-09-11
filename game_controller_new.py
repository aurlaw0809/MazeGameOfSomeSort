from game_objects_new import GameObject, Player
import pygame


class Game:
    def __init__(self, characters):
        self.player = (Player(self, 'fih', (0, 0), True, 50, False, 5))
        self.characters = characters
        self.backgrounds = []

    def set_up(self):
        pass

    def add_background_object(self, controller, name, pos, solid, size, transparent):
        self.backgrounds.append(GameObject(controller, name, pos, solid, size, transparent))

    def check_collisions(self):
        for thing in self.backgrounds:
            if pygame.(thing.get_collision_rect()).colliderect(self.player.get_collision_rect()):
                #TODO HERE HERE HERE
                if thing.get_solid():
                    return True
                else:
                    return False
        return False

    def scan_radius(self, pos, size, interaction_radius):
        possibilities = []
        for thing in self.backgrounds:
            if (thing.get_pos()[0] - pos[0])**2 + (thing.get_pos()[1] - pos[1])**2 <= (size + thing.get_size() + interaction_radius)**2:
                if thing.get_interactable():
                    possibilities.append(thing)
        return possibilities

    def move_character_by_key(self, character, key):
        move = False
        new_pos = character.find_next_location(key)
        size = character.get_size()
        if not self.check_collisions(new_pos, size):
            character.move(key)
            move = True
        return move

    def move_character_by_pos(self, character, pos):
        move = False
        size = character.get_size()
        if not self.check_collisions(pos, size):
            character.move_to_pos(pos)
            move = True
        return move

    def make_swap(self, character):
        if not self.check_collisions(character.get_s_end_pos(), character.get_size()):
            move_to = character.get_s_end_pos()

            self.move_character_by_pos(character, move_to)
            character.s_rotate_by(180)