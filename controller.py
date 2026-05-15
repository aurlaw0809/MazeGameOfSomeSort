from objects import Object, Character
import pygame

class Game:
    def __init__(self):
        self.characters = []
        self.backgrounds = []

    def check_collisions(self, pos):
        for thing in self.backgrounds:
            if thing.pos == pos:
                if thing.solid:
                    return True
                else:
                    return False
        return True
    #true = there IS a collision

    def move_character(self, character, key):
        mv = False
        new_pos = character.find_next_location(key)
        if not self.check_collisions(new_pos):
            character.move(key)
            mv = True
        return mv

    def switch_with_shadow(self, character):
        if character.get_shadow_direction() % 45 == 0:

        move_vector = pygame.Vector2(1, 0).rotate(character.get_shadow_direction())
        distance = character.get_size * (character.get_shadow_length - 1)

        character.move_by_vector(move_vector)

        character.update_shadow_direction(180)