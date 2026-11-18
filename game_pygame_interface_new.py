import pygame
from game_controller_new import Game

BACKGROUND_COLORS = {'W': (120, 176, 69),
                     'S': (204, 111, 61),
                     'E': (224, 176, 92),
                     'F': (219, 227, 127)
                     }
PLAYER_COLOR = (173, 39, 36)

SCREEN_SIZE = (640, 480)

GREEN_FROG_KEY = ['assets/doors/green_frog/1.png', 'assets/doors/green_frog/2.png', 'assets/doors/green_frog/3.png', 'assets/doors/green_frog/4.png', 'assets/doors/green_frog/5.png', 'assets/doors/green_frog/6.png']
BLUE_FROG_KEY = ['assets/doors/blue_frog/1.png', 'assets/doors/blue_frog/2.png', 'assets/doors/blue_frog/3.png', 'assets/doors/blue_frog/4.png', 'assets/doors/blue_frog/5.png', 'assets/doors/blue_frog/6.png']
BROWN_FROG_KEY = ['assets/doors/brown_frog/1.png', 'assets/doors/brown_frog/2.png', 'assets/doors/brown_frog/3.png', 'assets/doors/brown_frog/4.png', 'assets/doors/brown_frog/5.png', 'assets/doors/brown_frog/6.png']
YELLOW_FROG_KEY = ['assets/doors/yellow_frog/1.png', 'assets/doors/yellow_frog/2.png', 'assets/doors/yellow_frog/3.png', 'assets/doors/yellow_frog/4.png', 'assets/doors/yellow_frog/5.png', 'assets/doors/yellow_frog/6.png']

EXIT_DOOR = ['assets/doors/exit_door_closed.png', 'assets/doors/exit_door_open.png']
GREEN_WALL_2 = ['assets/walls/green_flowers/B2.png', 'assets/walls/green_flowers/T2.png']
STARCHY = {
            'S': ['assets/starchy/S0.png', 'assets/starchy/S1.png', 'assets/starchy/S2.png', 'assets/starchy/S3.png',
                  'assets/starchy/S4.png', 'assets/starchy/S5.png', 'assets/starchy/S6.png'],
            'A': ['assets/starchy/A0.png', 'assets/starchy/A1.png', 'assets/starchy/A2.png', 'assets/starchy/A3.png',
                  'assets/starchy/A4.png', 'assets/starchy/A5.png', 'assets/starchy/A6.png'],
            'D': ['assets/starchy/D0.png', 'assets/starchy/D1.png', 'assets/starchy/D2.png', 'assets/starchy/D3.png',
                  'assets/starchy/D4.png', 'assets/starchy/D5.png', 'assets/starchy/D6.png'],
            'W': ['assets/starchy/W0.png', 'assets/starchy/W1.png', 'assets/starchy/W2.png', 'assets/starchy/W3.png',
                  'assets/starchy/W4.png', 'assets/starchy/W5.png', 'assets/starchy/W6.png']}

PIXEL_SCALER = 2


class GameGUI:

    def __init__(self):

        pygame.init()
        pygame.display.set_caption('Maze testing')

        #set clock so that FPS can be limited
        self.clock = pygame.time.Clock()

        self.moving_by_click = False
        self.moving_by_key = False

        self.rotating_by_click = False
        self.rotating_by_key = False

        player_images = STARCHY

        self.starting_player_pos = (SCREEN_SIZE[0] // 2 - 50, SCREEN_SIZE[1] // 2)

        objects = []

        walls = [['wall_1', (500, 500), 16 * PIXEL_SCALER, GREEN_WALL_2],
                 ['wall_2', (500 + 32 * PIXEL_SCALER, 500), 16 * PIXEL_SCALER, GREEN_WALL_2],
                 ['wall_3', (500 - 32 * PIXEL_SCALER, 500), 16 * PIXEL_SCALER, GREEN_WALL_2]
                 ]

        player = ['starchy', self.starting_player_pos, 16 * PIXEL_SCALER, 10, player_images]

        keys = [['test_key', (100, 100), 11 * PIXEL_SCALER, GREEN_FROG_KEY, 'red', (500 + 16 * PIXEL_SCALER, 500),
                 17 * PIXEL_SCALER, EXIT_DOOR],
                ['test_key2', (0, 0), 11 * PIXEL_SCALER, BLUE_FROG_KEY, 'red', (500 - 16 * PIXEL_SCALER, 500),
                 17 * PIXEL_SCALER, EXIT_DOOR], ]

        self.bg = pygame.image.load("assets/test_bg/img.png")
        self.bg = pygame.transform.scale(self.bg, (800, 800))
        self.bg_rect = pygame.Rect(-100, -100, self.bg.get_width(), self.bg.get_height())

        self.screen = pygame.display.set_mode(SCREEN_SIZE)
        self.running = True
        self.offset = (0, 0)
        self.offset_speed = 10

        #order = A, D, S, W, O, P
        buttons = [[self.screen, 20, 430, 16 * PIXEL_SCALER, 16 * PIXEL_SCALER, 0, None, None, None, None, None, None, None, 'P', False, None, ['assets/buttons/a_key/1.png', 'assets/buttons/a_key/2.png']],
                   [self.screen, 20 + 16 * 2 * PIXEL_SCALER, 430, 16 * PIXEL_SCALER, 16 * PIXEL_SCALER, 0, None, None, None, None, None, None, None, 'P', False, None, ['assets/buttons/d_key/1.png', 'assets/buttons/d_key/2.png']],
                   [self.screen, 20 + 16 * PIXEL_SCALER, 430, 16 * PIXEL_SCALER, 16 * PIXEL_SCALER, 0, None, None, None, None, None, None, None, 'P', False, None, ['assets/buttons/s_key/1.png', 'assets/buttons/s_key/2.png']],
                   [self.screen, 20 + 16 * PIXEL_SCALER, 430 - 16 * PIXEL_SCALER, 16 * PIXEL_SCALER, 16 * PIXEL_SCALER, 0, None, None, None, None, None, None, None, 'P', False, None, ['assets/buttons/w_key/1.png', 'assets/buttons/w_key/2.png']],
                   [self.screen, 20 + 16 * 4 * PIXEL_SCALER, 430, 16 * PIXEL_SCALER, 16 * PIXEL_SCALER, 0, None, None, None, None, None, None, None, 'P', False, None, ['assets/buttons/o_key/1.png', 'assets/buttons/o_key/2.png']],
                   [self.screen, 20 + 16 * 5 * PIXEL_SCALER, 430, 16 * PIXEL_SCALER, 16 * PIXEL_SCALER, 0, None, None, None, None, None, None, None, 'P', False, None, ['assets/buttons/p_key/1.png', 'assets/buttons/p_key/2.png']],
                   [self.screen, 20 + 16 * 4 * PIXEL_SCALER, 430 - 16 * PIXEL_SCALER, 16 * PIXEL_SCALER, 16 * PIXEL_SCALER, 0, None, None, None, None, None, None, None, 'P', False, None, ['assets/buttons/k_key/1.png', 'assets/buttons/k_key/2.png']],
                   [self.screen, 20 + 16 * 5 * PIXEL_SCALER, 430 - 16 * PIXEL_SCALER, 16 * PIXEL_SCALER, 16 * PIXEL_SCALER, 0, None, None, None, None, None, None, None, 'P', False, None, ['assets/buttons/l_key/1.png', 'assets/buttons/l_key/2.png']],
                   [self.screen, 20 + 16 * 6 * PIXEL_SCALER, 430 - 16 * PIXEL_SCALER, 16 * PIXEL_SCALER, 16 * PIXEL_SCALER, 0, None, None, None, None, None, None, None, 'P', False, None, ['assets/buttons/space_key/1.png', 'assets/buttons/space_key/2.png']],
                   ]

        e_buttons = [[self.screen, 20 + 16 * 6 * PIXEL_SCALER, 430, 16 * PIXEL_SCALER, 16 * PIXEL_SCALER, 0, None, None, None, None, None, None, None, 'P', False, None, ['assets/buttons/e_key/1.png', 'assets/buttons/e_key/2.png']],
                    [self.screen, 20 + 16 * 6 * PIXEL_SCALER, 430, 16 * PIXEL_SCALER, 16 * PIXEL_SCALER, 0, None, None, None, None, None, None, None, 'P', False, None, ['assets/buttons/e_key_active/1.png', 'assets/buttons/e_key_active/2.png']]
                    ]

        #blue, brown, yellow, green
        scavenger = [[self.screen, 20 + 16 * 8 * PIXEL_SCALER, 430 - 16 * PIXEL_SCALER, 16 * PIXEL_SCALER, 16 * PIXEL_SCALER, 0, None, None, None, None, None, None, None, 'P', False, None, ['assets/buttons/frog_blue/1.png', 'assets/buttons/frog_blue/3.png', 'assets/buttons/frog_blue/2.png']],
                     [self.screen, 20 + 16 * 9 * PIXEL_SCALER, 430 - 16 * PIXEL_SCALER, 16 * PIXEL_SCALER, 16 * PIXEL_SCALER, 0, None, None, None, None, None, None, None, 'P', False, None, ['assets/buttons/frog_brown/1.png', 'assets/buttons/frog_brown/3.png', 'assets/buttons/frog_brown/2.png']],
                     [self.screen, 20 + 16 * 8 * PIXEL_SCALER, 430, 16 * PIXEL_SCALER, 16 * PIXEL_SCALER, 0, None, None, None, None, None, None, None, 'P', False, None, ['assets/buttons/frog_yellow/1.png', 'assets/buttons/frog_yellow/3.png', 'assets/buttons/frog_yellow/2.png']],
                     [self.screen, 20 + 16 * 9 * PIXEL_SCALER, 430, 16 * PIXEL_SCALER, 16 * PIXEL_SCALER, 0, None, None, None, None, None, None, None, 'P', False, None, ['assets/buttons/frog_green/1.png', 'assets/buttons/frog_green/3.png', 'assets/buttons/frog_green/2.png']],
                     ]

        self.game = Game(objects, keys, player, walls, buttons, e_buttons, scavenger)
        self.game.set_up()

        game_keys = self.game.get_keys()
        scavenger_buttons = self.game.get_scavenger()
        for i in range(len(game_keys)):
            if i == 0:
                game_keys[i].add_button(scavenger_buttons[3])
            if i == 1:
                game_keys[i].add_button(scavenger_buttons[0])

            print(game_keys[i])


        self.current_e_button = self.game.get_e_buttons()[0]

        self.player = self.game.player

        # self, screen, x, y,width, height, spacing,inactive_color, active_colour,text, text_color, text_font, text_x, text_y,button_type, toggled, user_text, images

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

                # key_options = {'pygame O': self.player.rotate, }
                # key_options[event.key]()

                if event.key == pygame.K_o:
                    self.player.set_rotating_ac(True)
                    self.rotating_by_key = True
                if event.key == pygame.K_p:
                    self.player.set_rotating_c(True)
                    self.rotating_by_key = True

                if event.key == pygame.K_SPACE:
                    self.old_pos = self.player.get_pos()
                    self.game.make_swap()

                if event.key == pygame.K_w:
                    self.player.set_direction('W')
                    self.player.set_moving(True)
                    self.moving_by_key = True
                if event.key == pygame.K_s:
                    self.player.set_direction('S')
                    self.player.set_moving(True)
                    self.moving_by_key = True
                if event.key == pygame.K_a:
                    self.player.set_direction('A')
                    self.player.set_moving(True)
                    self.moving_by_key = True
                if event.key == pygame.K_d:
                    self.player.set_direction('D')
                    self.player.set_moving(True)
                    self.moving_by_key = True

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

            if event.type == pygame.KEYUP and self.running:

                if event.key == pygame.K_o or event.key == pygame.K_p:
                    self.player.set_rotating_c(False)
                    self.player.set_rotating_ac(False)
                    self.rotating_by_key = False

                if event.key == pygame.K_w or event.key == pygame.K_s or event.key == pygame.K_a or event.key == pygame.K_d:
                    self.player.set_moving(False)
                    self.moving_by_key = False

            if event.type == pygame.MOUSEMOTION and self.running:

                for button in self.game.get_buttons():
                    if button.check_collision(event.pos):
                        button.make_active()
                    else:
                        button.make_inactive()

                if self.current_e_button.check_collision(event.pos):
                    self.current_e_button.make_active()
                else:
                    self.current_e_button.make_inactive()

            if event.type == pygame.MOUSEBUTTONDOWN and self.running:

                for i in range(len(self.game.get_buttons())):
                    button = self.game.buttons[i]
                    if button.check_collision(event.pos):
                        button.make_active()

                        #A, D, S, W, O, P, K, L
                        if i == 0:
                            self.player.set_direction('A')
                            self.player.set_moving(True)
                            self.moving_by_click = True
                        elif i == 1:
                            self.player.set_direction('D')
                            self.player.set_moving(True)
                            self.moving_by_click = True
                        elif i == 2:
                            self.player.set_direction('S')
                            self.player.set_moving(True)
                            self.moving_by_click = True
                        elif i == 3:
                            self.player.set_direction('W')
                            self.player.set_moving(True)
                            self.moving_by_click = True
                        elif i == 4:
                            self.player.set_rotating_ac(True)
                            self.rotating_by_click = True
                        elif i == 5:
                            self.player.set_rotating_c(True)
                            self.rotating_by_click = True
                        elif i == 6:
                            self.player.s_lengthen('K')
                        elif i == 7:
                            self.player.s_lengthen('L')
                        elif i == 8:
                            self.old_pos = self.player.get_pos()
                            self.game.make_swap()

                if self.current_e_button.check_collision(event.pos):
                    self.current_e_button.make_active()
                    possibilities = self.game.scan_radius()
                    if possibilities is None:
                        pass
                    else:
                        for object in possibilities:
                            object.interact()
                else:
                    self.current_e_button.make_inactive()

            if event.type == pygame.MOUSEBUTTONUP and self.running:

                if self.moving_by_click and not self.moving_by_key:
                    self.player.set_moving(False)

                if self.rotating_by_click and not self.rotating_by_key:
                    self.player.set_rotating_c(False)
                    self.player.set_rotating_ac(False)



    def _process_game_logic(self):
        if self.running and self.player.get_moving():
            for i in range(self.player.get_speed()):
                self.game.move_character_by_key(self.player.get_direction())
        if self.running and self.player.get_rotating_c():
            self.player.s_rotate('P')
        if self.running and self.player.get_rotating_ac():
            self.player.s_rotate('O')

        if self.game.scan_radius() is not None:
            self.current_e_button = self.game.get_e_buttons()[1]
        else:
            self.current_e_button = self.game.get_e_buttons()[0]

    def _draw(self):
        self.screen.fill((120, 176, 69))
        self.screen.blit(self.bg, pygame.Rect(-100 - self.offset[0], -100 - self.offset[1], self.bg.get_width(), self.bg.get_height()))
        self._draw_layering_properly()
        pygame.display.flip()


    def _draw_layering_properly(self):
        player_drawn = False
        shadow_drawn = False
        for thing in self.game.get_everything():
            if self.player.get_s_end_pos()[1] <= thing.get_pos()[1] and not shadow_drawn:
                self.player.draw_shadow_separate(self.screen, self.offset)
                shadow_drawn = True
            if self.player.get_pos()[1] <= thing.get_pos()[1] and not player_drawn:
                if not shadow_drawn:
                    self.player.draw_shadow_separate(self.screen, self.offset)
                    shadow_drawn = True
                self.player.draw_player_separate(self.screen, self.offset)
                player_drawn = True
            '''
            thing.draw_collision_rect(self.screen, self.offset)
            if thing.get_interactable():
                thing.draw_interaction_circle(self.screen, self.offset)
            '''

            thing.draw(self.screen, self.offset)
        if not shadow_drawn:
            self.player.draw_shadow_separate(self.screen, self.offset)
        if not player_drawn:
            self.player.draw_player_separate(self.screen, self.offset)

        for thing in self.game.get_ui():
            thing.draw()

        self.current_e_button.draw()




if __name__ == "__main__":
    game = GameGUI()
    game.main_loop()