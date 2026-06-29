from objects import GameObject, Player, Key, Door

class Game:
    def __init__(self):
        self.characters = []
        self.backgrounds = []

    def set_up(self):
        self.characters.append(Player(self, 'fih', (0, 0), True, 25, False, 5))

    def add_background_object(self, controller, name, pos, solid, size, transparent):
        self.backgrounds.append(GameObject(controller, name, pos, solid, size, transparent))

    def check_collisions(self, pos, size):
        for thing in self.backgrounds:
            if (thing.get_pos()[0] - pos[0])^2 + (thing.get_pos()[1] - pos[1])^2 <= (size + thing.get_size())^2:
                if thing.get_solid():
                    return True
                else:
                    return False
        return True

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