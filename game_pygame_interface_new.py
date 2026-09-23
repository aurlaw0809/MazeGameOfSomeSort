import pygame
from game_controller_new import Game

from pygame.locals import (
    K_LEFT,
    K_RIGHT,
    K_UP,
    K_DOWN,
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

        player_images = {
            'S': ['assets/starchy/S0.png', 'assets/starchy/S1.png', 'assets/starchy/S2.png', 'assets/starchy/S3.png',
                  'assets/starchy/S4.png', 'assets/starchy/S5.png', 'assets/starchy/S6.png'],
            'A': ['assets/starchy/A0.png', 'assets/starchy/A1.png', 'assets/starchy/A2.png', 'assets/starchy/A3.png',
                  'assets/starchy/A4.png', 'assets/starchy/A5.png', 'assets/starchy/A6.png'],
            'D': ['assets/starchy/D0.png', 'assets/starchy/D1.png', 'assets/starchy/D2.png', 'assets/starchy/D3.png',
                  'assets/starchy/D4.png', 'assets/starchy/D5.png', 'assets/starchy/D6.png'],
            'W': ['assets/starchy/W0.png', 'assets/starchy/W1.png', 'assets/starchy/W2.png', 'assets/starchy/W3.png',
                  'assets/starchy/W4.png', 'assets/starchy/W5.png', 'assets/starchy/W6.png']}

        self.screen = pygame.display.set_mode((500, 500))
        self.game = Game(None, None, player_images)
        self.game.set_up()
        self.running = True

        self.player = self.game.player

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
                    self.player.set_rotating_ac(True)
                if event.key == pygame.K_p:
                    self.player.set_rotating_c(True)

                if event.key == pygame.K_SPACE:
                    self.game.make_swap()

                if event.key == pygame.K_w:
                    self.player.set_direction('W')
                    self.player.set_moving(True)
                if event.key == pygame.K_s:
                    self.player.set_direction('S')
                    self.player.set_moving(True)
                if event.key == pygame.K_a:
                    self.player.set_direction('A')
                    self.player.set_moving(True)
                if event.key == pygame.K_d:
                    self.player.set_direction('D')
                    self.player.set_moving(True)

                if event.key == pygame.K_k:
                    self.player.s_lengthen('K')
                if event.key == pygame.K_l:
                    self.player.s_lengthen('L')

                if event.key == pygame.K_e:
                    possibilities = self.game.scan_radius()
                    if possibilities is None:
                        pass
                    else:
                        pass

            if event.type == pygame.KEYUP:

                if event.key == pygame.K_o or event.key == pygame.K_p:
                    self.player.set_rotating_c(False)
                    self.player.set_rotating_ac(False)

                if event.key == pygame.K_w or event.key == pygame.K_s or event.key == pygame.K_a or event.key == pygame.K_d:
                    self.player.set_moving(False)

    def _process_game_logic(self):
        if self.running and self.player.get_moving():
            self.game.move_character_by_key(self.player.get_direction())
        if self.running and self.player.get_rotating_c():
            self.player.s_rotate('P')
        if self.running and self.player.get_rotating_ac():
            self.player.s_rotate('O')

    def _draw(self):
        self.screen.fill((120, 176, 69))
        self.player.draw_player(self.screen)
        self._draw_characters()
        pygame.display.flip()

    def _draw_characters(self):
        pass



if __name__ == "__main__":
    game = GameGUI()
    game.main_loop()