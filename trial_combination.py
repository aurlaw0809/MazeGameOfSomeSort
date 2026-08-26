import pygame
from dynamic_bg_class import DynamicBackground
from button_class import ButtonList

pygame.init()

clock = pygame.time.Clock()
FPS = 60

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

BUTTON_TEXT_COLOUR = (255, 255, 255)
BUTTON_TEXT_FONT = pygame.font.SysFont('comicsans', 30)

BUTTON_TEXT_X = 10
BUTTON_TEXT_Y = 5

BUTTON_INACTIVE_COLOUR = (255, 255, 255, 50)
BUTTON_ACTIVE_COLOUR = (255, 255, 255, 100)

BUTTON_WIDTH = 200
BUTTON_HEIGHT = 50

BUTTON_X = 200
BUTTON_Y = 200

BUTTON_SPACING = 25

BUTTON_NAMES = ['BUTTON 1', 'BUTTON 2']
NUMBER_OF_BUTTONS = len(BUTTON_NAMES)

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
pygame.display.set_caption("Trialing combo")

bg = DynamicBackground(screen)
buttons = ButtonList(screen, BUTTON_X, BUTTON_Y,
                     BUTTON_WIDTH, BUTTON_HEIGHT, BUTTON_SPACING,
                     NUMBER_OF_BUTTONS, BUTTON_NAMES,
                     BUTTON_INACTIVE_COLOUR, BUTTON_ACTIVE_COLOUR,
                     BUTTON_TEXT_COLOUR, BUTTON_TEXT_FONT, BUTTON_TEXT_X, BUTTON_TEXT_Y)

run =True

while run:

    clock.tick(FPS)

    bg.draw()
    buttons.draw()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        if event.type == pygame.MOUSEMOTION:
            i = 0
            for i in range(0, buttons.get_number_buttons()):
                if buttons.get_list_buttons()[i].check_collision(event.pos):
                    buttons.set_active_button(i)

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                i = 0
                for i in range(0, buttons.get_number_buttons()):
                    if buttons.get_list_buttons()[i].check_collision(event.pos):
                        buttons.set_active_button(i)
                    if buttons.get_list_buttons()[i].is_active():
                        buttons.set_button_selected(True)
                        buttons.set_chosen_button(i)

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                if buttons.get_active_button() != -1:
                    buttons.set_chosen_button(buttons.get_active_button())
                    buttons.set_button_selected(True)

            if event.key == pygame.K_SPACE:
                if buttons.get_active_button() != -1:
                    buttons.set_active_button(buttons.get_active_button() + 1)
                else:
                    buttons.set_active_button(0)

            if event.key == pygame.K_ESCAPE:
                run = False
            if event.key == pygame.K_q:
                run = False

    pygame.display.update()

pygame.quit()