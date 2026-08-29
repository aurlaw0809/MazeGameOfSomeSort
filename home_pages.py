import pygame
from dynamic_bg_class import DynamicBackground
from button_class import ButtonList
import sqlite3
from db_commands import *
from home_pages_functions import *

#-----------------------------------------------------------------------------------------------------------------------------------

NORMAL_MUSIC_VOLUME = 0.5
NORMAL_SOUND_EFFECT_VOLUME = 0.2

pygame.init()
pygame.mixer.init()

pygame.mixer.music.load("assets/music/steven_universe.mp3")
pygame.mixer.music.set_volume(NORMAL_MUSIC_VOLUME)

click_sound = pygame.mixer.Sound("assets/sound_effects/click.wav")
click_sound.set_volume(NORMAL_SOUND_EFFECT_VOLUME)

keyboard3 = pygame.mixer.Sound("assets/sound_effects/keyboard3.wav")
keyboard2 = pygame.mixer.Sound("assets/sound_effects/keyboard2.wav")

keyboard2.set_volume(NORMAL_SOUND_EFFECT_VOLUME)
keyboard3.set_volume(NORMAL_SOUND_EFFECT_VOLUME)

keyboard_sounds = [keyboard2, keyboard3]

clock = pygame.time.Clock()
FPS = 60

SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 600

POP_UP_COLOUR = (255, 255, 255, 50)
POP_UP_CORNER_DISTANCE = 100
POP_UP_WIDTH = SCREEN_WIDTH - POP_UP_CORNER_DISTANCE * 2
POP_UP_HEIGHT = SCREEN_HEIGHT - POP_UP_CORNER_DISTANCE * 2

CORNER_DISTANCE = 50

BUTTON_TEXT_COLOUR = (255, 255, 255)
BUTTON_TEXT_FONT = pygame.font.Font('assets/fonts/pressstart2p.ttf', 20)

BUTTON_TEXT_X = 10
BUTTON_TEXT_Y = 10

BUTTON_INACTIVE_COLOUR = (255, 255, 255, 0)
BUTTON_ACTIVE_COLOUR = (255, 255, 255, 50)

BUTTON_WIDTH = 350
BUTTON_HEIGHT = 40

BUTTON_SPACING = 10

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
pygame.display.set_caption("Trialing combo")

bg = DynamicBackground(screen, 'sky1')

#B = branch, F = finish game, T = toggle, E = entry, L = level, C = close pop up, BC = branch and confirm name change
#pop up codes: E = username exists, C = confirm change, X = box left empty
# page name: [button names, action: to which page or toggle a variable or store a text box value, page type]

pages = {'SP2': [['NEXT', 'QUIT', 'ENTER NAME'], ['MM', None, None], ['B', 'F', 'E'], 4],
         'SP1': [['QUIT', 'ENTER NAME'], [None, None], ['F', 'E'], 3],
         'MM': [['START', 'SETTINGS', 'LEADERBOARD', 'QUIT'], ['MSS', 'MO', 'MRS', None], ['B', 'B', 'B', 'F'], 4],
         'MO': [['BACK', 'MUSIC', 'SOUND EFFECTS', 'NAME'], ['MM', True, True, None], ['B', 'T', 'T', 'E'], 5],
         'MRS': [['BACK', 'LVL. 1', 'LVL. 2', 'LVL. 3'], ['MM', None, None, None], ['B', 'L', 'L', 'L'], 4],
         'MRD': [['BACK'], ['MRS'], ['B'], 1],
         'MSS': [['BACK', 'LEVELS', 'TUTORIAL'], ['MM', 'MLS', None], ['B', 'B', 'L'], 3],
         'MLS': [['BACK', 'LVL. 1', 'LVL. 2', 'LVL. 3'], ['MSS', None, None, None], ['B', 'L', 'L', 'L'], 4],}

pop_ups = {'SP1E': [['BACK', 'YES'], ['SP1', 'SP2'], ['C', 'BC'], 2, 'Username is already on record, is this you?'],
           'SP1C': [['BACK', 'YES'], ['SP1', 'SP2'], ['C', 'BC'], 2, 'Confirm username?'],
           'SP1X': [['BACK'], ['SP1'], ['C'], 1, 'Username cannot be empty.'],

           'SP2E': [['BACK', 'YES'], ['SP2', 'SP2'], ['C', 'BC'], 2, 'Username is already on record, is this you?'],
           'SP2C': [['BACK', 'YES'], ['SP2', 'SP2'], ['C', 'BC'], 2, 'Confirm username?'],
           'SP2X': [['BACK'], ['SP2'], ['C'], 1, 'Username cannot be empty.'],

           'MOE': [['BACK', 'YES'], ['MO', 'MO'], ['C', 'BC'], 2, 'Username is already on record, is this you?'],
           'MOC': [['BACK', 'YES'], ['MO', 'MO'], ['C', 'BC'], 2, 'Confirm username?'],
           'MOX': [['BACK'], ['MO'], ['C'], 1, 'Username cannot be empty.'],}

current_page = 'SP1'
current_pop_up = ''

#-----------------------------------------------------------------------------------------------------------------------------------

def update_page(current_page):
    BUTTON_NAMES = pages[current_page][0]
    BUTTON_ACTIONS = pages[current_page][1]
    BUTTON_TYPES = pages[current_page][2]
    NUMBER_OF_BUTTONS = len(BUTTON_NAMES)
    BUTTON_Y = SCREEN_HEIGHT - (BUTTON_HEIGHT + BUTTON_SPACING) * pages[current_page][3] - CORNER_DISTANCE
    BUTTON_X = BUTTON_SPACING + CORNER_DISTANCE

    buttons = ButtonList(screen, BUTTON_X, BUTTON_Y,
                     BUTTON_WIDTH, BUTTON_HEIGHT, BUTTON_SPACING,
                     NUMBER_OF_BUTTONS, BUTTON_NAMES, BUTTON_TYPES, BUTTON_ACTIONS,
                     BUTTON_INACTIVE_COLOUR, BUTTON_ACTIVE_COLOUR,
                     BUTTON_TEXT_COLOUR, BUTTON_TEXT_FONT, BUTTON_TEXT_X, BUTTON_TEXT_Y)

    return buttons

def update_pop_ups(p_current_pop_up):

    if p_current_pop_up != '':

        BUTTON_NAMES = pop_ups[p_current_pop_up][0]
        BUTTON_ACTIONS = pop_ups[p_current_pop_up][1]
        BUTTON_TYPES = pop_ups[p_current_pop_up][2]
        NUMBER_OF_BUTTONS = len(BUTTON_NAMES)
        BUTTON_Y = SCREEN_HEIGHT - (BUTTON_HEIGHT + BUTTON_SPACING) * pop_ups[p_current_pop_up][3] - POP_UP_CORNER_DISTANCE
        BUTTON_X = BUTTON_SPACING + POP_UP_CORNER_DISTANCE

        pop_up_buttons = ButtonList(screen, BUTTON_X, BUTTON_Y,
                             BUTTON_WIDTH, BUTTON_HEIGHT, BUTTON_SPACING,
                             NUMBER_OF_BUTTONS, BUTTON_NAMES, BUTTON_TYPES, BUTTON_ACTIONS,
                             BUTTON_INACTIVE_COLOUR, BUTTON_ACTIVE_COLOUR,
                             BUTTON_TEXT_COLOUR, BUTTON_TEXT_FONT, BUTTON_TEXT_X, BUTTON_TEXT_Y)

    else:
        pop_up_buttons = None

    return pop_up_buttons

def draw_pop_ups(p_current_pop_up, pop_up_buttons):

    if p_current_pop_up != '':

        surface = pygame.Surface((POP_UP_WIDTH, POP_UP_HEIGHT), pygame.SRCALPHA)
        surface.fill(POP_UP_COLOUR)
        screen.blit(surface, (POP_UP_CORNER_DISTANCE, POP_UP_CORNER_DISTANCE))

        pop_up_buttons.draw()

        text = BUTTON_TEXT_FONT.render(f"{pop_ups[current_pop_up][4]}", True, BUTTON_TEXT_COLOUR)
        screen.blit(text, (POP_UP_CORNER_DISTANCE + BUTTON_SPACING, POP_UP_CORNER_DISTANCE + BUTTON_SPACING))

#-----------------------------------------------------------------------------------------------------------------------------------

run = True

text_box_selected = False
pop_up_selected = False

sound_effects_running = True
music_running = True

buttons = update_page(current_page)
pop_up_buttons = update_pop_ups(current_pop_up)

start_page = True
initial_name_done = False

user_name = ''

pygame.mixer.music.play(-1)

while run:

    clock.tick(FPS)

    bg.draw()
    buttons.draw()
    draw_pop_ups(current_pop_up, pop_up_buttons)

    if music_running:
        pygame.mixer.music.set_volume(NORMAL_MUSIC_VOLUME)
    else:
        pygame.mixer.music.set_volume(0)

    if sound_effects_running:
        keyboard2.set_volume(NORMAL_SOUND_EFFECT_VOLUME)
        keyboard3.set_volume(NORMAL_SOUND_EFFECT_VOLUME)
        click_sound.set_volume(NORMAL_SOUND_EFFECT_VOLUME)
    else:
        keyboard2.set_volume(0)
        keyboard3.set_volume(0)
        click_sound.set_volume(0)

 # -----------------------------------------------------------------------------------------------------------------------------------

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            run = False

# -----------------------------------------------------------------------------------------------------------------------------------

        if event.type == pygame.MOUSEMOTION:

            if not pop_up_selected and not text_box_selected:
                for i in range(0, buttons.get_number_buttons()):
                    if buttons.get_list_buttons()[i].check_collision(event.pos) and not text_box_selected:
                        buttons.set_active_button(i)

            elif pop_up_selected and current_pop_up != '':
                for i in range(0, pop_up_buttons.get_number_buttons()):
                    if pop_up_buttons.get_list_buttons()[i].check_collision(event.pos) and not text_box_selected:
                        pop_up_buttons.set_active_button(i)

# -----------------------------------------------------------------------------------------------------------------------------------

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:

                if not pop_up_selected and not text_box_selected and not start_page:
                    for i in range(0, buttons.get_number_buttons()):
                        if buttons.get_list_buttons()[i].is_active():
                            buttons.set_button_selected(True)
                            buttons.set_chosen_button(i)
                            click_sound.play()

                            if buttons.get_chosen_button_type() == 'T':
                                buttons.get_list_buttons()[i].switch_toggled()
                                pages = update_toggle(buttons, current_page, pages)
                                sound_effects_running, music_running = update_sounds_running(buttons, current_page, sound_effects_running, music_running)

                            elif buttons.get_chosen_button_type() == 'E':
                                buttons.get_list_buttons()[buttons.get_chosen_button()].selected_text_box()
                                text_box_selected = True

                            elif buttons.get_chosen_button_type() == 'B':
                                current_page = route_to_next_page(buttons, current_page, pages)
                                buttons = update_page(current_page)
                                break

                            elif buttons.get_chosen_button_type() == 'F':
                                run = False

                elif pop_up_selected:
                    for i in range(0, pop_up_buttons.get_number_buttons()):
                        if pop_up_buttons.get_list_buttons()[i].is_active():
                            pop_up_buttons.set_button_selected(True)
                            pop_up_buttons.set_chosen_button(i)
                            click_sound.play()

                            if pop_up_buttons.get_chosen_button_type() == 'BC':

                                test_name = buttons.get_list_buttons()[buttons.get_chosen_button()].get_user_text()
                                buttons.get_list_buttons()[buttons.get_chosen_button()].unselected_text_box()

                                user_name = test_name
                                pages['SP1'][1][1] = test_name
                                pages['SP2'][1][2] = test_name
                                pages['MO'][1][3] = test_name

                                if current_page == 'SP1':
                                    start_page = False

                                current_page = route_to_next_page(pop_up_buttons, current_pop_up, pop_ups)
                                buttons = update_page(current_page)
                                pop_up_selected = False
                                current_pop_up = ''
                                pop_up_buttons = update_pop_ups(current_pop_up)
                                break

                            elif pop_up_buttons.get_chosen_button_type() == 'C':

                                buttons.get_list_buttons()[buttons.get_chosen_button()].set_user_text(user_name)
                                buttons.get_list_buttons()[buttons.get_chosen_button()].unselected_text_box()

                                pop_up_selected = False
                                current_pop_up = ''
                                pop_up_buttons = update_pop_ups(current_pop_up)
                                break


                elif start_page:
                    for i in range(0, buttons.get_number_buttons()):
                        if buttons.get_list_buttons()[i].is_active():
                            buttons.set_button_selected(True)
                            buttons.set_chosen_button(i)
                            click_sound.play()

                            if buttons.get_chosen_button_type() == 'E':
                                buttons.get_list_buttons()[buttons.get_chosen_button()].selected_text_box()
                                text_box_selected = True

                            elif buttons.get_chosen_button_type() == 'F':
                                run = False

# -----------------------------------------------------------------------------------------------------------------------------------

        if event.type == pygame.KEYDOWN:
            random_keyboard_sound(keyboard_sounds).play()

            if not pop_up_selected and not text_box_selected:
                if event.key == pygame.K_RETURN:
                    if buttons.get_active_button() != -1:
                        buttons.set_chosen_button(buttons.get_active_button())
                        buttons.set_button_selected(True)
                        click_sound.play()

                        if buttons.get_chosen_button_type() == 'T':
                            user_name = buttons.get_list_buttons()[buttons.get_chosen_button()].get_user_text()
                            buttons.get_list_buttons()[buttons.get_chosen_button()].switch_toggled()
                            pages = update_toggle(buttons, current_page, pages)
                            sound_effects_running, music_running = update_sounds_running(buttons, current_page, sound_effects_running, music_running)

                        elif buttons.get_chosen_button_type() == 'E':
                            buttons.get_list_buttons()[buttons.get_chosen_button()].selected_text_box()
                            text_box_selected = True

                        elif buttons.get_chosen_button_type() == 'B' and not start_page:
                            current_page = route_to_next_page(buttons, current_page, pages)
                            buttons = update_page(current_page)
                            break

                        elif buttons.get_chosen_button_type() == 'F':
                            run = False

                if event.key == pygame.K_SPACE:
                    if buttons.get_active_button() != -1:
                        buttons.set_active_button(buttons.get_active_button() + 1)
                    else:
                        buttons.set_active_button(0)

                if event.key == pygame.K_ESCAPE:
                    if current_page == 'MM' or current_page == 'SP2' or current_page == 'SP1':
                        run = False
                    else:
                        buttons.set_active_button(0)
                        buttons.set_chosen_button(0)
                        current_page = route_to_next_page(buttons, current_page, pages)
                        buttons = update_page(current_page)

            elif pop_up_selected:
                if event.key == pygame.K_RETURN:
                    if pop_up_buttons.get_active_button() != -1:
                        pop_up_buttons.set_chosen_button(pop_up_buttons.get_active_button())
                        pop_up_buttons.set_button_selected(True)
                        click_sound.play()

                        if pop_up_buttons.get_chosen_button_type() == 'BC':

                            test_name = buttons.get_list_buttons()[buttons.get_chosen_button()].get_user_text()
                            buttons.get_list_buttons()[buttons.get_chosen_button()].unselected_text_box()

                            user_name = test_name
                            pages['SP1'][1][1] = test_name
                            pages['SP2'][1][2] = test_name
                            pages['MO'][1][3] = test_name

                            if current_page == 'SP1':
                                start_page = False

                            current_page = route_to_next_page(pop_up_buttons, current_pop_up, pop_ups)
                            buttons = update_page(current_page)
                            pop_up_selected = False
                            current_pop_up = ''
                            pop_up_buttons = update_pop_ups(current_pop_up)
                            break

                        elif pop_up_buttons.get_chosen_button_type() == 'C':

                            buttons.get_list_buttons()[buttons.get_chosen_button()].set_user_text(user_name)
                            buttons.get_list_buttons()[buttons.get_chosen_button()].unselected_text_box()

                            pop_up_selected = False
                            current_pop_up = ''
                            pop_up_buttons = update_pop_ups(current_pop_up)
                            break

                if event.key == pygame.K_SPACE:
                    if pop_up_buttons.get_active_button() != -1:
                        pop_up_buttons.set_active_button(pop_up_buttons.get_active_button() + 1)
                    else:
                        pop_up_buttons.set_active_button(0)

                if event.key == pygame.K_ESCAPE:
                    pop_up_buttons.set_chosen_button(0)
                    current_page = route_to_next_page(pop_up_buttons, current_pop_up, pop_ups)
                    buttons = update_page(current_page)
                    pop_up_selected = False
                    current_pop_up = ''
                    pop_up_buttons = update_pop_ups(current_pop_up)
                    break

            elif text_box_selected:
                if event.key == pygame.K_BACKSPACE:
                    buttons.get_list_buttons()[buttons.get_chosen_button()].backspace_user_text()
                elif event.unicode.isprintable() and event.key != pygame.K_SPACE and buttons.get_list_buttons()[
                    buttons.get_chosen_button()].get_len_user_text() < 30:
                    buttons.get_list_buttons()[buttons.get_chosen_button()].add_user_text(event.unicode)
                elif event.key == pygame.K_RETURN:
                    test_name = buttons.get_list_buttons()[buttons.get_chosen_button()].get_user_text()

                    if len(test_name) == 0 and len(user_name) == 0:
                        pop_up_selected = True
                        text_box_selected = False
                        current_pop_up = f'{current_page}X'
                        pop_up_buttons = update_pop_ups(current_pop_up)

                    elif len(test_name) == 0 or user_name == test_name:
                        buttons.get_list_buttons()[buttons.get_chosen_button()].set_user_text(user_name)
                        buttons.get_list_buttons()[buttons.get_chosen_button()].unselected_text_box()
                        text_box_selected = False

                    elif validate_user_name_input(test_name):
                        text_box_selected = False
                        pop_up_selected = True
                        current_pop_up = f'{current_page}C'
                        pop_up_buttons = update_pop_ups(current_pop_up)

                    else:
                        pop_up_selected = True
                        buttons.get_list_buttons()[buttons.get_chosen_button()].unselected_text_box()
                        text_box_selected = False
                        current_pop_up = f'{current_page}E'
                        pop_up_buttons = update_pop_ups(current_pop_up)

                        #need to add if making input user_name as global variable :)

    pygame.display.update()

pygame.quit()