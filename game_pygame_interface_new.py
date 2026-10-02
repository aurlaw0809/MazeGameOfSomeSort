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

        self.starting_player_pos = (200, 250)

        objects = [['test_block', (100, 100), 50, True, False, False, None, None]]
        player = ['starchy', self.starting_player_pos, 50, 10, player_images]

        self.bg = pygame.image.load("assets/test_bg/img.png")
        self.bg = pygame.transform.scale(self.bg, (1000, 1000))
        self.bg_rect = pygame.Rect(-100, -100, self.bg.get_width(), self.bg.get_height())

        self.screen = pygame.display.set_mode((500, 500))
        self.game = Game(objects, None, player)
        self.game.set_up()
        self.running = True
        self.offset = (0, 0)
        self.dragging_offset = False
        self.dragging_offset_distance = (0, 0)

        self.player = self.game.player

    def main_loop(self):
        while self.running:
            self._update_offset()
            self._handle_input()
            self._process_game_logic()
            self._draw()
            self.clock.tick(60)# cap to 60 FPS
        pygame.quit()

    def _update_offset(self):
        if not self.dragging_offset:
            self.offset = (int(self.player.get_pos()[0] - self.starting_player_pos[0]), int(self.player.get_pos()[1] - self.starting_player_pos[1]))
        else:
            if self.offset[0] != int(self.player.get_pos()[0] - self.starting_player_pos[0]):
                self.offset = (int(self.offset[0] + self.dragging_offset_distance[0]), self.offset[1])
            if self.offset[1] != int(self.player.get_pos()[1] - self.starting_player_pos[1]):
                self.offset = (self.offset[0], int(self.offset[1] + self.dragging_offset_distance[1]))
            if self.offset == (int(self.player.get_pos()[0] - self.starting_player_pos[0]), int(self.player.get_pos()[1] - self.starting_player_pos[1])):
                self.dragging_offset = False
                self.dragging_offset_distance = (0, 0)

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
                    self.old_pos = self.player.get_pos()
                    if self.game.make_swap():
                        self.dragging_offset = True
                        if int(self.player.get_pos()[0] - self.old_pos[0]) > 0:
                            x = 1
                        elif int(self.player.get_pos()[0] - self.old_pos[0]) == 0:
                            x = 0
                        else:
                            x = -1
                        if int(self.player.get_pos()[1] - self.old_pos[1]) > 0:
                            y = 1
                        elif int(self.player.get_pos()[1] - self.old_pos[1]) == 0:
                            y = 0
                        else:
                            y = -1
                        self.dragging_offset_distance = (x, y)

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
        self.screen.blit(self.bg, pygame.Rect(-100 - self.offset[0], -100 - self.offset[1], self.bg.get_width(), self.bg.get_height()))
        self._draw_objects()
        self.player.draw_player(self.screen, self.offset)
        pygame.display.flip()

    def _draw_objects(self):
        for thing in self.game.get_background_objects():
            thing.draw_collision_rect(self.screen, self.offset)



if __name__ == "__main__":
    game = GameGUI()
    game.main_loop()