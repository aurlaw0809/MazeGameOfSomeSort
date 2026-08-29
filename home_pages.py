#-----------------------------------------------------------------------------------------------------------------------------------
#LIBRARIES

import pygame
from dynamic_bg_class import DynamicBackground
from button_class import ButtonList
from home_pages_functions import *

pygame.init()
pygame.mixer.init()

#-----------------------------------------------------------------------------------------------------------------------------------
#CONSTANTS

NORMAL_MUSIC_VOLUME = 0.5
NORMAL_SOUND_EFFECT_VOLUME = 0.2

clock = pygame.time.Clock()
FPS = 60

SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 600

POP_UP_COLOUR = (249, 219, 207)
POP_UP_CORNER_DISTANCE = 100
POP_UP_WIDTH = SCREEN_WIDTH - POP_UP_CORNER_DISTANCE * 2
POP_UP_HEIGHT = SCREEN_HEIGHT - POP_UP_CORNER_DISTANCE * 2
POP_UP_TEXT_COLOUR = (183, 93, 100)
POP_UP_BUTTON_INACTIVE_COLOUR = (244, 183, 149, 0)
POP_UP_BUTTON_ACTIVE_COLOUR = (244, 183, 149, 50)

CORNER_DISTANCE = 50

BUTTON_TEXT_COLOUR = (255, 255, 255)
BUTTON_TEXT_FONT = pygame.font.Font('assets/fonts/pressstart2p.ttf', 20)

BUTTON_TEXT_X = 10
BUTTON_TEXT_Y = 10

BUTTON_INACTIVE_COLOUR = (249, 219, 207, 0)
BUTTON_ACTIVE_COLOUR = (249, 219, 207, 50)

BUTTON_WIDTH = 350
BUTTON_HEIGHT = 40

BUTTON_SPACING = 10

#-----------------------------------------------------------------------------------------------------------------------------------
#SOUND SET UP

bg_music = ["assets/music/lease_frutiger_aero.mp3", "assets/music/dont_stop_till_you_get_enough.mp3", "assets/music/elevator_music.mp3"]
bg_index = random.randint(0, len(bg_music) - 1)

pygame.mixer.music.load(bg_music[bg_index])
pygame.mixer.music.set_volume(NORMAL_MUSIC_VOLUME)

CLICK_SOUND = pygame.mixer.Sound("assets/sound_effects/click.wav")
CLICK_SOUND.set_volume(NORMAL_SOUND_EFFECT_VOLUME)

KEYBOARD1 = pygame.mixer.Sound("assets/sound_effects/keyboard3.wav")
KEYBOARD2 = pygame.mixer.Sound("assets/sound_effects/keyboard2.wav")

KEYBOARD2.set_volume(NORMAL_SOUND_EFFECT_VOLUME)
KEYBOARD1.set_volume(NORMAL_SOUND_EFFECT_VOLUME)

#-----------------------------------------------------------------------------------------------------------------------------------
#OTHER SET UP

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
pygame.display.set_caption("Trialing combo")

bg = DynamicBackground(screen, 'sky1')

#-----------------------------------------------------------------------------------------------------------------------------------
#SOME DICTIONARIES AND LISTS

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

keyboard_sounds = [KEYBOARD2, KEYBOARD1]

#-----------------------------------------------------------------------------------------------------------------------------------
#SOME FUNCTIONS THAT USE CONSTANTS SO ARE IN THIS FILE

def update_page(p_current_page, p_pages):
    button_names = p_pages[p_current_page][0]
    button_actions = p_pages[p_current_page][1]
    button_types = p_pages[p_current_page][2]
    number_of_buttons = len(button_names)
    button_y = SCREEN_HEIGHT - (BUTTON_HEIGHT + BUTTON_SPACING) * p_pages[p_current_page][3] - CORNER_DISTANCE
    button_x = BUTTON_SPACING + CORNER_DISTANCE

    p_buttons = ButtonList(screen, button_x, button_y,
                     BUTTON_WIDTH, BUTTON_HEIGHT, BUTTON_SPACING,
                     number_of_buttons, button_names, button_types, button_actions,
                     BUTTON_INACTIVE_COLOUR, BUTTON_ACTIVE_COLOUR,
                     BUTTON_TEXT_COLOUR, BUTTON_TEXT_FONT, BUTTON_TEXT_X, BUTTON_TEXT_Y)

    return p_buttons

def update_pop_ups(p_current_pop_up, p_pop_ups):

    if p_current_pop_up != '':

        pop_up_button_names = p_pop_ups[p_current_pop_up][0]
        pop_up_button_actions = p_pop_ups[p_current_pop_up][1]
        pop_up_button_types = p_pop_ups[p_current_pop_up][2]
        pop_up_number_of_buttons = len(pop_up_button_names)
        pop_up_button_y = SCREEN_HEIGHT - (BUTTON_HEIGHT + BUTTON_SPACING) * p_pop_ups[p_current_pop_up][3] - POP_UP_CORNER_DISTANCE
        pop_up_button_x = BUTTON_SPACING + POP_UP_CORNER_DISTANCE

        p_pop_up_buttons = ButtonList(screen, pop_up_button_x, pop_up_button_y,
                             BUTTON_WIDTH, BUTTON_HEIGHT, BUTTON_SPACING,
                             pop_up_number_of_buttons, pop_up_button_names, pop_up_button_types, pop_up_button_actions,
                             POP_UP_BUTTON_INACTIVE_COLOUR, POP_UP_BUTTON_ACTIVE_COLOUR,
                             POP_UP_TEXT_COLOUR, BUTTON_TEXT_FONT, BUTTON_TEXT_X, BUTTON_TEXT_Y)

    else:
        p_pop_up_buttons = None

    return p_pop_up_buttons

def draw_pop_ups(p_current_pop_up, p_pop_up_buttons):

    if p_current_pop_up != '':

        surface = pygame.Surface((POP_UP_WIDTH, POP_UP_HEIGHT), pygame.SRCALPHA)
        surface.fill(POP_UP_COLOUR)
        screen.blit(surface, (POP_UP_CORNER_DISTANCE, POP_UP_CORNER_DISTANCE))

        p_pop_up_buttons.draw()

        text = BUTTON_TEXT_FONT.render(f"{pop_ups[p_current_pop_up][4]}", True, POP_UP_TEXT_COLOUR)
        screen.blit(text, (POP_UP_CORNER_DISTANCE + BUTTON_SPACING + BUTTON_TEXT_X, POP_UP_CORNER_DISTANCE + BUTTON_SPACING + BUTTON_TEXT_Y))

def pop_up_choose_bc(p_buttons, p_current_page, p_start_page, p_pop_up_buttons, p_current_pop_up, p_pop_ups, p_pages):

    p_test_name = p_buttons.get_list_buttons()[p_buttons.get_chosen_button()].get_user_text()
    p_buttons.get_list_buttons()[p_buttons.get_chosen_button()].unselected_text_box()

    submit_new_user_name_input(p_test_name)
    p_user_name = p_test_name
    p_pages['SP1'][1][1] = p_test_name
    p_pages['SP2'][1][2] = p_test_name
    p_pages['MO'][1][3] = p_test_name

    if p_current_page == 'SP1':
        p_start_page = False

    p_current_page = route_to_next_page(p_pop_up_buttons, p_current_pop_up, p_pop_ups)
    p_buttons = update_page(p_current_page, p_pages)
    p_pop_up_selected = False
    p_current_pop_up = ''
    p_pop_up_buttons = update_pop_ups(p_current_pop_up, p_pop_ups)

    return p_buttons, p_current_page, p_start_page, p_user_name, p_pop_up_buttons, p_current_pop_up, p_pop_ups, p_pop_up_selected

def pop_up_choose_c(p_buttons, p_user_name, p_pop_ups):

    p_buttons.get_list_buttons()[p_buttons.get_chosen_button()].set_user_text(p_user_name)
    p_buttons.get_list_buttons()[p_buttons.get_chosen_button()].unselected_text_box()

    p_pop_up_selected = False
    p_current_pop_up = ''
    p_pop_up_buttons = update_pop_ups(p_current_pop_up, p_pop_ups)

    return p_buttons, p_pop_up_selected, p_current_pop_up, p_pop_up_buttons

#-----------------------------------------------------------------------------------------------------------------------------------
#VARIABLES

run = True

current_page = 'SP1'
current_pop_up = ''

text_box_selected = False
pop_up_selected = False

sound_effects_running = True
music_running = True

buttons = update_page(current_page, pages)
pop_up_buttons = update_pop_ups(current_pop_up, pop_ups)

start_page = True

user_name = ''

pygame.mixer.music.play(-1)

#-----------------------------------------------------------------------------------------------------------------------------------
#MAIN LOOP

while run:

    clock.tick(FPS)

#-----------------------------------------------------------------------------------------------------------------------------------
#DRAWING WINDOWS

    bg.draw()
    buttons.draw()
    draw_pop_ups(current_pop_up, pop_up_buttons)

#-----------------------------------------------------------------------------------------------------------------------------------
#MUSIC AND SOUND EFFECT JAZZ

    if music_running:
        pygame.mixer.music.set_volume(NORMAL_MUSIC_VOLUME)
    else:
        pygame.mixer.music.set_volume(0)

    if sound_effects_running:
        KEYBOARD2.set_volume(NORMAL_SOUND_EFFECT_VOLUME)
        KEYBOARD1.set_volume(NORMAL_SOUND_EFFECT_VOLUME)
        CLICK_SOUND.set_volume(NORMAL_SOUND_EFFECT_VOLUME)
    else:
        KEYBOARD2.set_volume(0)
        KEYBOARD1.set_volume(0)
        CLICK_SOUND.set_volume(0)

# -----------------------------------------------------------------------------------------------------------------------------------
#START PYGAME.GET

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            run = False

# -----------------------------------------------------------------------------------------------------------------------------------
#MOUSE MOTION

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
#MOUSE BUTTON DOWN

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:

                if not pop_up_selected and not text_box_selected and not start_page:
                    for i in range(0, buttons.get_number_buttons()):
                        if buttons.get_list_buttons()[i].is_active():
                            buttons.set_button_selected(True)
                            buttons.set_chosen_button(i)
                            CLICK_SOUND.play()

                            if buttons.get_chosen_button_type() == 'T':
                                buttons.get_list_buttons()[i].switch_toggled()
                                pages = update_toggle(buttons, current_page, pages)
                                sound_effects_running, music_running = update_sounds_running(buttons, current_page, sound_effects_running, music_running)

                            elif buttons.get_chosen_button_type() == 'E':
                                buttons.get_list_buttons()[buttons.get_chosen_button()].selected_text_box()
                                text_box_selected = True

                            elif buttons.get_chosen_button_type() == 'B':
                                current_page = route_to_next_page(buttons, current_page, pages)
                                buttons = update_page(current_page, pages)
                                break

                            elif buttons.get_chosen_button_type() == 'F':
                                run = False

                elif pop_up_selected:
                    for i in range(0, pop_up_buttons.get_number_buttons()):
                        if pop_up_buttons.get_list_buttons()[i].is_active():
                            pop_up_buttons.set_button_selected(True)
                            pop_up_buttons.set_chosen_button(i)
                            CLICK_SOUND.play()

                            if pop_up_buttons.get_chosen_button_type() == 'BC':

                                buttons, current_page, start_page, user_name, pop_up_buttons, current_pop_up, pop_ups, pop_up_selected = pop_up_choose_bc(
                                    buttons, current_page, start_page, pop_up_buttons, current_pop_up, pop_ups, pages)
                                break

                            elif pop_up_buttons.get_chosen_button_type() == 'C':

                                buttons, pop_up_selected, current_pop_up, pop_up_buttons = pop_up_choose_c(
                                    buttons, user_name, pop_ups)
                                break


                elif start_page:
                    for i in range(0, buttons.get_number_buttons()):
                        if buttons.get_list_buttons()[i].is_active():
                            buttons.set_button_selected(True)
                            buttons.set_chosen_button(i)
                            CLICK_SOUND.play()

                            if buttons.get_chosen_button_type() == 'E':
                                buttons.get_list_buttons()[buttons.get_chosen_button()].selected_text_box()
                                text_box_selected = True

                            elif buttons.get_chosen_button_type() == 'F':
                                run = False

# -----------------------------------------------------------------------------------------------------------------------------------
#KEYDOWN

        if event.type == pygame.KEYDOWN:
            random_keyboard_sound(keyboard_sounds).play()

            if not pop_up_selected and not text_box_selected:
                if event.key == pygame.K_RETURN:
                    if buttons.get_active_button() != -1:
                        buttons.set_chosen_button(buttons.get_active_button())
                        buttons.set_button_selected(True)
                        CLICK_SOUND.play()

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
                            buttons = update_page(current_page, pages)
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
                        buttons = update_page(current_page, pages)

            elif pop_up_selected:
                if event.key == pygame.K_RETURN:
                    if pop_up_buttons.get_active_button() != -1:
                        pop_up_buttons.set_chosen_button(pop_up_buttons.get_active_button())
                        pop_up_buttons.set_button_selected(True)
                        CLICK_SOUND.play()

                        if pop_up_buttons.get_chosen_button_type() == 'BC':

                            buttons, current_page, start_page, user_name, pop_up_buttons, current_pop_up, pop_ups, pop_up_selected = pop_up_choose_bc(
                                buttons, current_page, start_page, pop_up_buttons, current_pop_up, pop_ups, pages)
                            break

                        elif pop_up_buttons.get_chosen_button_type() == 'C':

                            buttons, pop_up_selected, current_pop_up, pop_up_buttons = pop_up_choose_c(
                                buttons, user_name, pop_ups)
                            break

                if event.key == pygame.K_SPACE:
                    if pop_up_buttons.get_active_button() != -1:
                        pop_up_buttons.set_active_button(pop_up_buttons.get_active_button() + 1)
                    else:
                        pop_up_buttons.set_active_button(0)

                if event.key == pygame.K_ESCAPE:
                    pop_up_buttons.set_chosen_button(0)
                    current_page = route_to_next_page(pop_up_buttons, current_pop_up, pop_ups)
                    buttons = update_page(current_page, pages)
                    pop_up_selected = False
                    current_pop_up = ''
                    pop_up_buttons = update_pop_ups(current_pop_up, pop_ups)
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
                        pop_up_buttons = update_pop_ups(current_pop_up, pop_ups)

                    elif len(test_name) == 0 or user_name == test_name:
                        buttons.get_list_buttons()[buttons.get_chosen_button()].set_user_text(user_name)
                        buttons.get_list_buttons()[buttons.get_chosen_button()].unselected_text_box()
                        text_box_selected = False

                    elif validate_user_name_input(test_name):
                        text_box_selected = False
                        pop_up_selected = True
                        current_pop_up = f'{current_page}C'
                        pop_up_buttons = update_pop_ups(current_pop_up, pop_ups)

                    else:
                        pop_up_selected = True
                        buttons.get_list_buttons()[buttons.get_chosen_button()].unselected_text_box()
                        text_box_selected = False
                        current_pop_up = f'{current_page}E'
                        pop_up_buttons = update_pop_ups(current_pop_up, pop_ups)

# -----------------------------------------------------------------------------------------------------------------------------------
#END OF CODE

    pygame.display.update()

pygame.quit()