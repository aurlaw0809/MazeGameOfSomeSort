import pygame
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
        self.player_image = pygame.image.load('goldfish.png').convert_alpha()
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
                if event.key == pygame.K_s:
                    self.move_direction = 'S'
                if event.key == pygame.K_a:
                    self.move_direction = 'A'
                if event.key == pygame.K_d:
                    self.move_direction = 'D'

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
                    self.player.s_snap_angle()

                if event.key == pygame.K_w or event.key == pygame.K_s or event.key == pygame.K_a or event.key == pygame.K_d:
                    self.move_direction = None

    def _process_game_logic(self):
        if self.running and self.move_direction is not None:
            self.game.move_character_by_key(self.player, self.move_direction)
        if self.running and self.rotating_c:
            self.player.s_rotate('P')
        if self.running and self.rotating_ac:
            self.player.s_rotate('O')

    def _draw(self):
        self.screen.fill((120, 176, 69))
        self._draw_shadow()
        self._draw_characters()
        pygame.display.flip()

    def _draw_characters(self):
        self.player_rect.center = (self.player.pos[0], self.player.pos[1])
        self.screen.blit(self.player_image, self.player_rect)
        for character in self.game.characters:
            pass #update this when there's actually more than one character

    def _draw_shadow(self):

        shadow_length = self.player.get_s_length()
        if shadow_length == 0:
            return

        angle = self.player.get_s_angle()
        move_vector = pygame.Vector2(1, 0).rotate(angle)
        maximum_distance = shadow_length * self.player.get_size()

        surface_size = maximum_distance*2
        shadow_surface = pygame.Surface((surface_size, surface_size), pygame.SRCALPHA)

        centre_x = surface_size // 2
        centre_y = surface_size // 2

        for x in range(self.player.get_size()):
            for y in range(self.player.get_size()):

                #get pixel and ignore if transparent
                pixel = self.player_image.get_at((x, y))
                if pixel.a == 0:
                    continue

                x_displacement = ((self.player.get_size() - x) / self.player.get_size() * maximum_distance)
                y_displacement = ((self.player.get_size() - y) / self.player.get_size() * maximum_distance)

                draw_x = int(centre_x + move_vector.x * x_displacement)
                draw_y = int(centre_y + move_vector.y * y_displacement)

                shadow_surface.set_at((draw_x, draw_y), self.shadow_colour)

        #reference rectangle
        rect = pygame.Rect(0, 0, surface_size, surface_size)
        rect.center = (self.player.pos[0], self.player.pos[1] + self.player.get_size() / 2)
        pygame.draw.rect(self.screen, (255, 0, 0), rect)

        shadow_rect = shadow_surface.get_rect()
        shadow_rect.center = (self.player.pos[0], self.player.pos[1] + self.player.get_size() / 2)
        self.screen.blit(shadow_surface, shadow_rect)

if __name__ == "__main__":
    game = GameGUI()
    game.main_loop()