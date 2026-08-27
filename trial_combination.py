import pygame
from dynamic_bg_class import DynamicBackground
from button_class import ButtonList

pygame.init()

clock = pygame.time.Clock()
FPS = 60

SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 600

BUTTON_TEXT_COLOUR = (255, 255, 255)
BUTTON_TEXT_FONT = pygame.font.Font('assets/fonts/pressstart2p.ttf', 20)

BUTTON_TEXT_X = 10
BUTTON_TEXT_Y = 10

BUTTON_INACTIVE_COLOUR = (255, 255, 255, 0)
BUTTON_ACTIVE_COLOUR = (255, 255, 255, 100)

BUTTON_WIDTH = 350
BUTTON_HEIGHT = 40

BUTTON_X = 30
BUTTON_Y = 300

BUTTON_SPACING = 10

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
pygame.display.set_caption("Trialing combo")

bg = DynamicBackground(screen)

#B = branch, F = finish game, T = toggle, E = entry, L = level
# page name: [button names, action: to which page or toggle a variable or store a text box value, page type]

pages = {'MM': [['START', 'SETTINGS', 'LEADERBOARD', 'QUIT'], ['MSS', 'MO', 'MRS', None], ['B', 'B', 'B', 'F']],
         'MO': [['BACK', 'MUSIC', 'SOUND EFFECTS', 'NAME'], ['MM', False, False, None], ['B', 'T', 'T', 'E']],
         'MRS': [['BACK', 'LVL. 1', 'LVL. 2', 'LVL. 3'], ['MM', None, None, None], ['B', 'L', 'L', 'L']],
         'MRD': [['BACK'], ['MRS'], ['B']],
         'MSS': [['BACK', 'LEVELS', 'TUTORIAL'], ['MM', 'MLS', None], ['B', 'B', 'L']],
         'MLS': [['BACK', 'LVL. 1', 'LVL. 2', 'LVL. 3'], ['MSS', None, None, None], ['B', 'L', 'L', 'L']],}

current_page = 'MM'

def update_page():
    BUTTON_NAMES = pages[current_page][0]
    BUTTON_ACTIONS = pages[current_page][1]
    BUTTON_TYPES = pages[current_page][2]
    NUMBER_OF_BUTTONS = len(BUTTON_NAMES)

    buttons = ButtonList(screen, BUTTON_X, BUTTON_Y,
                     BUTTON_WIDTH, BUTTON_HEIGHT, BUTTON_SPACING,
                     NUMBER_OF_BUTTONS, BUTTON_NAMES, BUTTON_TYPES, BUTTON_ACTIONS,
                     BUTTON_INACTIVE_COLOUR, BUTTON_ACTIVE_COLOUR,
                     BUTTON_TEXT_COLOUR, BUTTON_TEXT_FONT, BUTTON_TEXT_X, BUTTON_TEXT_Y)

    return buttons

def route_to_next_page(buttons, current_page):
    button_number = buttons.get_chosen_button()
    options = pages[current_page][1]
    new_page = options[button_number]

    if new_page == None:
        new_page = current_page

    return new_page

def update_toggle(buttons, current_page, pages_list):
    button_number = buttons.get_chosen_button()
    toggle_value = buttons.get_list_buttons()[button_number].get_toggled()

    pages_list[current_page][1][button_number] = toggle_value

    return pages_list



run =True
buttons = update_page()

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
                    if buttons.get_list_buttons()[i].is_active():
                        buttons.set_button_selected(True)
                        buttons.set_chosen_button(i)

                        #check here

                        if buttons.get_chosen_button_type() == 'T':
                            buttons.get_list_buttons()[i].switch_toggled()
                            pages = update_toggle(buttons, current_page, pages)
                        
                        if buttons.get_chosen_button_type() == 'B':
                            current_page = route_to_next_page(buttons, current_page)
                            buttons = update_page()
                            break


        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                if buttons.get_active_button() != -1:
                    buttons.set_chosen_button(buttons.get_active_button())
                    buttons.set_button_selected(True)

                    if buttons.get_chosen_button_type() == 'T':
                        buttons.get_list_buttons()[buttons.get_chosen_button()].switch_toggled()
                        pages = update_toggle(buttons, current_page, pages)

                    if buttons.get_chosen_button_type() == 'B':
                        current_page = route_to_next_page(buttons, current_page)
                        buttons = update_page()
                        break

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