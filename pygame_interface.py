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

        # Set clock so that FPS can be limited
        self.clock = pygame.time.Clock()

        self.game = Game()
        self.game.set_up()
        self.move_direction: str | None = None

        self.screen = pygame.display.set_mode([500, 500])
        self.running = True

        self.player = self.game.characters[0]
        self.player_image = pygame.image.load('fish.png').convert_alpha()
        self.player_image = pygame.transform.scale(self.player_image, (50, 50))
        self.player_rect = self.player_image.get_rect()

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
        """ Checks key presses and adjusts GameGUI attributes depending on the presses """

        for event in pygame.event.get():

            if event.type == pygame.QUIT or event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False

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
                    self.player.s_length('K')
                if event.key == pygame.K_l:
                    self.player.s_length('L')

            if event.type == pygame.KEYUP:

                if event.key == pygame.K_o or event.key == pygame.K_p:
                    self.rotating_c = False
                    self.rotating_ac = False
                    self.player.s_snap_angle()

                if event.key == pygame.K_w or event.key == pygame.K_s or event.key == pygame.K_a or event.key == pygame.K_d:
                    self.move_direction = None

            # Checks for movement keys amd sets self.move_direction according to the key pressed.
            # Otherwise, set self.move_direction to None

    def _process_game_logic(self):
        """ Implements character moves and checks if player has reached the exit """
        if self.running and self.move_direction is not None:
            self.game.move_character_by_key(self.player, self.move_direction)
        if self.running and self.rotating_c:
            self.player.s_rotate('P')
        if self.running and self.rotating_ac:
            self.player.s_rotate('O')

    def _draw(self):
        """draw background first then characters"""
        self._draw_characters()
        pygame.display.flip()

    def _draw_characters(self):
        """Loop through the characters and draw a circle for each character"""
        for character in self.game.characters:
            self.player_rect.center = (self.player.pos[0], self.player.pos[1])
            self.screen.blit(self.player_image, self.player_rect)

if __name__ == "__main__":
    game = GameGUI()
    game.main_loop()