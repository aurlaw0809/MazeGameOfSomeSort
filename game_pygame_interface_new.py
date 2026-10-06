import pygame
from game_controller_new import Game

BACKGROUND_COLORS = {'W': (120, 176, 69),
                     'S': (204, 111, 61),
                     'E': (224, 176, 92),
                     'F': (219, 227, 127)
                     }
PLAYER_COLOR = (173, 39, 36)

SCREEN_SIZE = (640, 480)

class GameGUI:

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

        self.starting_player_pos = (SCREEN_SIZE[0] // 2 - 50, SCREEN_SIZE[1] // 2)

        objects = [['test_block', (100, 100), 50, True, False, False, None, None]]
        player = ['starchy', self.starting_player_pos, 50, 10, player_images]
        keys = [['test_key', (50, 50), 25, 'assets/placeholder_door/key.png', 'red', (1000, 1000), 200, ['assets/placeholder_door/closed_door.png', 'assets/placeholder_door/open_door.png']]]

        self.bg = pygame.image.load("assets/test_bg/img.png")
        self.bg = pygame.transform.scale(self.bg, (800, 800))
        self.bg_rect = pygame.Rect(-100, -100, self.bg.get_width(), self.bg.get_height())

        self.screen = pygame.display.set_mode(SCREEN_SIZE)
        self.game = Game(objects, keys, player)
        self.game.set_up()
        self.running = True
        self.offset = (0, 0)
        self.offset_speed = 10

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
        aim_offset = (self.player.get_pos()[0] - self.starting_player_pos[0], self.player.get_pos()[1] - self.starting_player_pos[1])

        x_change = self.offset[0] - aim_offset[0]
        if abs(x_change) < self.offset_speed:
            x_change = -x_change
        elif x_change < 0:
            x_change = self.offset_speed
        elif x_change > 0:
            x_change = -self.offset_speed
        else:
            x_change = 0

        y_change = self.offset[1] - aim_offset[1]
        if abs(y_change) < self.offset_speed:
            y_change = -y_change
        elif y_change < 0:
            y_change = self.offset_speed
        elif y_change > 0:
            y_change = -self.offset_speed
        else:
            y_change = 0

        self.offset = (self.offset[0] + x_change, self.offset[1] + y_change)

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
                        for object in possibilities:
                            object.interact()

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
        self._draw_keys()
        self.player.draw_player(self.screen, self.offset)
        pygame.display.flip()

    def _draw_objects(self):
        for thing in self.game.get_background_objects():
            thing.draw_collision_rect(self.screen, self.offset)

    def _draw_keys(self):
        for thing in self.game.get_keys():
            thing.draw_key(self.screen, self.offset)
            thing.door.draw_door(self.screen, self.offset)
            #thing.door.draw_collision_rect(self.screen, self.offset)




if __name__ == "__main__":
    game = GameGUI()
    game.main_loop()