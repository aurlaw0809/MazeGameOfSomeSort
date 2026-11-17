from game_objects_new import GameObject, Player, Key, Wall
from button_class import Button
import pygame

#TODO BUTTONS

class Game:
    def __init__(self, objects, keys, player, walls, buttons, e_buttons):
        self.player = (Player(self, player[0], player[1], player[2], player[3], player[4]))
        self.backgrounds = []
        self.walls = []
        self.keys = []
        self.everything = []

        self.e_buttons = []

        self.buttons = []
        self.ui = []

        if objects is not None:
            for obj in objects:
                self.add_background_object(obj)
        if keys is not None:
            for key in keys:
                self.add_key(key)
        if walls is not None:
            for wall in walls:
                self.add_wall(wall)

        if buttons is not None:
            for button in buttons:
                self.add_button(button)
        if e_buttons is not None:
            for button in e_buttons:
                self.add_e_buttons(button)




    def set_up(self):
        pass

    def add_background_object(self, obj):
        self.backgrounds.append(GameObject(self, obj[0], obj[1], obj[2], obj[3], obj[4], obj[5], obj[6], obj[7]))
        #controller, name, pos, size, solid, transparent, interactable, image, colour
        self.add_into_everything(self.backgrounds[-1])

    def add_key(self, key):
        self.keys.append(Key(self, key[0], key[1], key[2], key[3], key[4], key[5], key[6], key[7]))
        #controller, name, pos, size, image, colour, door_pos, door_size, door_images'
        self.add_into_everything(self.keys[-1])
        self.add_into_everything((self.keys[-1]).door)

    def add_wall(self, wall):
        self.walls.append(Wall(self, wall[0], wall[1], wall[2], wall[3]))
        self.add_into_everything(self.walls[-1])

    def add_button(self, button):
        self.buttons.append(Button(button[0], button[1], button[2], button[3], button[4], button[5], button[6], button[7], button[8], button[9], button[10], button[11], button[12], button[13], button[14], button[15], button[16]))
        self.add_into_ui(self.buttons[-1])

    def add_e_buttons(self, button):
        self.e_buttons.append(Button(button[0], button[1], button[2], button[3], button[4], button[5], button[6], button[7], button[8], button[9], button[10], button[11], button[12], button[13], button[14], button[15], button[16]))

    def add_into_ui(self, object):
        self.ui.append(object)

    def add_into_everything(self, object):
        inserted = False
        if len(self.everything) > 0:
            for i in range(len(self.everything)):
                if object.get_pos()[1] <= self.everything[i].get_pos()[1] and not inserted:
                    self.everything.insert(i, object)
                    inserted = True
                if not inserted:
                    self.everything.append(object)
        else:
            self.everything.append(object)

    def get_background_objects(self):
        return self.backgrounds

    def get_keys(self):
        return self.keys

    def get_buttons(self):
        return self.buttons
    def get_e_buttons(self):
        return self.e_buttons

    def get_everything(self):
        return self.everything

    def get_ui(self):
        return self.ui

    def check_collisions(self, new_pos):
        new_rect = pygame.Rect(new_pos[0] + self.player.get_size() / 4, new_pos[1] - self.player.get_size() / 2, self.player.get_size() / 2, self.player.get_size() / 2)
        for thing in self.backgrounds:
            if pygame.Rect.colliderect(new_rect, thing.get_collision_rect()):
                if thing.get_solid():
                    return True
        for door in self.keys:
            if pygame.Rect.colliderect(new_rect, door.door.get_collision_rect()):
                if door.door.get_solid():
                    return True
        for wall in self.walls:
            if pygame.Rect.colliderect(new_rect, wall.get_collision_rect()):
                if wall.get_solid():
                    return True
        return False

    def scan_radius(self):
        possibilities = []
        for thing in self.backgrounds:
            if thing.get_interactable():
                if (((thing.get_pos()[0] + thing.get_size() / 2) - (self.player.get_pos()[0] + self.player.get_size() / 2))**2 +
                        ((thing.get_pos()[1] + thing.get_size() / 2) - (self.player.get_pos()[1] - self.player.get_size() / 2))**2 <= (thing.get_interaction_radius())**2):
                    possibilities.append(thing)

        for key in self.keys:
            if (((key.get_pos()[0] + key.get_size() / 2) - (self.player.get_pos()[0] + self.player.get_size() / 2)) ** 2 +
                    ((key.get_pos()[1] - key.get_size() / 2) - (self.player.get_pos()[1] - self.player.get_size() / 2)) ** 2 <= (key.get_interaction_radius()) ** 2):
                if not key.get_key_found():
                    possibilities.append(key)

            front_entry = False
            back_entry = False

            if (((key.door.get_pos()[0] + key.door.get_size() / 2) - (self.player.get_pos()[0] + self.player.get_size() / 2)) ** 2 +
                ((key.door.get_pos()[1]) - (self.player.get_pos()[1] - self.player.get_size() / 2)) ** 2 <= (key.door.get_interaction_radius()) ** 2):
                front_entry = True
            if (((key.door.get_pos()[0] + key.door.get_size() / 2) - (self.player.get_pos()[0] + self.player.get_size() / 2)) ** 2 +
                ((key.door.get_pos()[1] - key.door.get_size()) - (self.player.get_pos()[1] - self.player.get_size() / 2)) ** 2 <= (key.door.get_interaction_radius()) ** 2):
                back_entry = True

            if back_entry or front_entry:
                if not key.door.get_door_open():
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