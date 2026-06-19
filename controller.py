from objects import GameObject, Player, Key, Door

class Game:
    def __init__(self):
        self.characters = []
        self.backgrounds = []

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

    def check_valid_swap(self, p_pos, s_pos, s_size):
        if not self.check_collisions(s_pos, s_size):
            p_pos = s_pos

    def move_character(self, character, key):
        move = False
        new_pos = character.find_next_location(key)
        size = character.get_size()
        if not self.check_collisions(new_pos, size):
            character.move(key)
            move = True
        return move