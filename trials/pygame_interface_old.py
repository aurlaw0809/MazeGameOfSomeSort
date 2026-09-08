import pygame
import math
import numpy as np
from controller import Game

from pygame.locals import (
    K_LEFT,
    K_RIGHT,
    K_UP,
    K_DOWN,
    K_ESCAPE,
    KEYDOWN,
    QUIT,
    KEYUP,
)

BACKGROUND_COLORS = {'W': (120, 176, 69),
                     'S': (204, 111, 61),
                     'E': (224, 176, 92),
                     'F': (219, 227, 127)
                     }
PLAYER_COLOR = (173, 39, 36)


def shear_image(image, offset):

    width, height = image.get_size()

    new_width = width + abs(offset)
    result = pygame.Surface((new_width, height), pygame.SRCALPHA)

    for y in range(height):
        x_offset = int(offset * (height - y) / height)

        if offset < 0:
            x_offset += abs(offset)

        for x in range(width):
            pixel = image.get_at((x, y))
            result.set_at((int(x + x_offset), int(y)), pixel)

    return result


def shadow_image(image, size, colour):

    new_image = pygame.Surface((size, size), pygame.SRCALPHA)
    for y in range(size):
        for x in range(size):
            pixel = image.get_at((x, y))
            if pixel.a == 0:
                continue

            new_image.set_at((x, y), colour)

    return new_image


class GameGUI:
    key_moves = {K_UP: 'W',
                 K_DOWN: 'S',
                 K_RIGHT: 'A',
                 K_LEFT: 'D',
                 }

    def __init__(self):
        pygame.init()
        pygame.display.set_caption('Maze testing')

        #set clock so that FPS can be limited
        self.clock = pygame.time.Clock()

        self.game = Game()
        self.game.set_up() #
        self.move_direction: str | None = None

        self.screen = pygame.display.set_mode((500, 500))
        self.running = True

        #player image

        self.player = self.game.characters[0]

        self.player_direction = 'S'
        self.player_moving = False
        self.player_moving_frame = 0
        self.player_images = {'S': ['assets/starchy/S0.png', 'assets/starchy/S1.png', 'assets/starchy/S2.png', 'assets/starchy/S3.png', 'assets/starchy/S4.png', 'assets/starchy/S5.png', 'assets/starchy/S6.png'],
                              'A': ['assets/starchy/A0.png', 'assets/starchy/A1.png', 'assets/starchy/A2.png', 'assets/starchy/A3.png', 'assets/starchy/A4.png', 'assets/starchy/A5.png', 'assets/starchy/A6.png'],
                              'D': ['assets/starchy/D0.png', 'assets/starchy/D1.png', 'assets/starchy/D2.png', 'assets/starchy/D3.png', 'assets/starchy/D4.png', 'assets/starchy/D5.png', 'assets/starchy/D6.png'],
                              'W': ['assets/starchy/W0.png', 'assets/starchy/W1.png', 'assets/starchy/W2.png', 'assets/starchy/W3.png', 'assets/starchy/W4.png', 'assets/starchy/W5.png', 'assets/starchy/W6.png']}
        self.direction_order = ['S', 'A', 'W', 'D']
        self.walking_slower = 0

        self.player_image = pygame.image.load(self.player_images[self.player_direction][self.player_moving_frame]).convert_alpha()
        self.player_image = pygame.transform.scale(self.player_image, (self.player.get_size(), self.player.get_size()))
        self.player_rect = self.player_image.get_rect()

        self.shadow_colour = (30, 30, 30, 100)

        self.rotating_c = False
        self.rotating_ac = False

    def main_loop(self):
        while self.running:
            self._handle_input()
            self._process_game_logic()
            self._draw()
            self.clock.tick(60) # cap to 60 FPS
        pygame.quit()

    def _handle_input(self):
        for event in pygame.event.get():

            if event.type == pygame.QUIT or event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.running = False

            if event.type == pygame.KEYDOWN and self.running:

                if event.key == pygame.K_o:
                    self.rotating_ac = True
                if event.key == pygame.K_p:
                    self.rotating_c = True

                if event.key == pygame.K_SPACE:
                    self.game.make_swap(self.player)

                if event.key == pygame.K_w:
                    self.move_direction = 'W'
                    self.player_direction = 'W'
                    self.player_moving = True
                if event.key == pygame.K_s:
                    self.move_direction = 'S'
                    self.player_direction = 'S'
                    self.player_moving = True
                if event.key == pygame.K_a:
                    self.move_direction = 'A'
                    self.player_direction = 'A'
                    self.player_moving = True
                if event.key == pygame.K_d:
                    self.move_direction = 'D'
                    self.player_direction = 'D'
                    self.player_moving = True

                if event.key == pygame.K_k:
                    self.player.s_lengthen('K')
                if event.key == pygame.K_l:
                    self.player.s_lengthen('L')

                if event.key == pygame.K_e:
                    self.game.scan_radius(self.player.get_pos(), self.player.get_size(), self.player.get_interaction_radius())

            if event.type == pygame.KEYUP:

                if event.key == pygame.K_o or event.key == pygame.K_p:
                    self.rotating_c = False
                    self.rotating_ac = False
                    #self.player.s_snap_angle()

                if event.key == pygame.K_w or event.key == pygame.K_s or event.key == pygame.K_a or event.key == pygame.K_d:
                    self.move_direction = None
                    self.player_moving = False

    def _process_game_logic(self):
        if self.running and self.move_direction is not None:
            self.game.move_character_by_key(self.player, self.move_direction)
        if self.running and self.rotating_c:
            self.player.s_rotate('P')
        if self.running and self.rotating_ac:
            self.player.s_rotate('O')

    def _draw(self):
        self.screen.fill((120, 176, 69))
        self._draw_full_shadow()
        self._draw_characters()
        pygame.display.flip()

    def _draw_characters(self):

        if self.player_moving:
            self.walking_slower += 1
            self.walking_slower %= 8
            if self.walking_slower == 0:
                self.player_moving_frame += 1
                self.player_moving_frame %= 7
        else:
            self.player_moving_frame = 0

        self.player_rect.center = (self.player.pos[0], self.player.pos[1])
        self.player_image = pygame.image.load(self.player_images[self.player_direction][self.player_moving_frame]).convert_alpha()
        self.player_image = pygame.transform.scale(self.player_image, (self.player.get_size(), self.player.get_size()))
        self.screen.blit(self.player_image, self.player_rect)
        for character in self.game.characters:
            pass #update this when there's actually more than one character

    def _draw_shadow(self, image, xmod, ymod, rotation, side):

        size = self.player.get_size()
        height = self.player.get_s_length()
        colour = self.shadow_colour
        angle = self.player.get_s_angle()

        move_vector = pygame.Vector2(height * size, 0).rotate((angle + rotation)%360)
        image = shadow_image(image, size, colour)
        image = pygame.transform.smoothscale(image, (size, abs(move_vector.y)))

        offset = move_vector.x
        image = shear_image(image, offset)

        image = pygame.transform.rotate(image, rotation)

        corner_x = 0
        corner_y = 0

        if not side:
            if 270 <= angle <= 360 or 0 <= angle <= 90:
                corner_x = self.player.pos[0] - self.player.get_size() / 2
            else:
                corner_x = self.player.pos[0] - self.player.get_size() / 2 + offset

            if 0 <= angle <= 180:
                corner_y = self.player.pos[1] + self.player.get_size() / 2
                image = pygame.transform.flip(image, False, True)
            else:
                corner_y = self.player.pos[1] + self.player.get_size() / 2 + move_vector.y

            corner_x += xmod * self.player.get_size()

        if side:
            if 90 <= angle <= 270:
                corner_x = self.player.pos[0] - image.get_width()
                corner_x += xmod * self.player.get_size()
            else:
                corner_x = self.player.pos[0]
                corner_x -= xmod * self.player.get_size()
                image = pygame.transform.flip(image, True, False)

            if 180 <= angle <= 360:
                corner_y = self.player.pos[1] + self.player.get_size() / 2 - image.get_height()
            else:
                corner_y = self.player.pos[1] - self.player.get_size() / 2

        corner_y += ymod * self.player.get_size()

        """
        background = pygame.Surface(image.get_size(), pygame.SRCALPHA)
        background.fill((255, 0, 0, 255))
        self.screen.blit(background, (corner_x, corner_y))
        """

        self.screen.blit(image, (corner_x, corner_y))

    def _draw_full_shadow(self):
        image = self.player_image

        index = self.direction_order.index(self.player_direction)

        front_shadow = self.player_image

        back_shadow = pygame.image.load(self.player_images[self.direction_order[(index + 2)%4]][self.player_moving_frame]).convert_alpha()
        back_shadow = pygame.transform.scale(back_shadow, (self.player.get_size(), self.player.get_size()))
        back_shadow = pygame.transform.flip(back_shadow, True, False)

        left_shadow = pygame.image.load(self.player_images[self.direction_order[(index + 1)%4]][self.player_moving_frame]).convert_alpha()
        left_shadow = pygame.transform.scale(left_shadow, (self.player.get_size(), self.player.get_size()))

        right_shadow = pygame.image.load(self.player_images[self.direction_order[(index + 3)%4]][self.player_moving_frame]).convert_alpha()
        right_shadow = pygame.transform.scale(right_shadow, (self.player.get_size(), self.player.get_size()))
        right_shadow = pygame.transform.flip(right_shadow, True, False)

        self._draw_shadow(front_shadow, 0, 0, 0, False)

        """
        if self.player_direction == 'S' or self.player_direction == 'W':
            self._draw_shadow(back_shadow, 0, -0.3, 0, False)
            self._draw_shadow(left_shadow, 0.3, 0.4, 90, True)
            self._draw_shadow(right_shadow, -0.3, 0.4, 90, True)
        else:
            self._draw_shadow(back_shadow, 0, -0.7, 0, False)
            self._draw_shadow(left_shadow, 0.1, 0.1, 90, True)
            self._draw_shadow(right_shadow, -0.1, 0.1, 90, True)
        """


if __name__ == "__main__":
    game = GameGUI()
    game.main_loop()