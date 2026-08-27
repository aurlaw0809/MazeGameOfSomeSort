import pygame
import random
from dynamic_bg_class import DynamicBackground
from button_class import ButtonList

pygame.init()
pygame.mixer.init()

pygame.mixer.music.load("assets/music/steven_universe.mp3")
pygame.mixer.music.set_volume(0.5)

click_sound = pygame.mixer.Sound("assets/sound_effects/click.wav")
click_sound.set_volume(0.2)

keyboard3 = pygame.mixer.Sound("assets/sound_effects/keyboard3.wav")
keyboard2 = pygame.mixer.Sound("assets/sound_effects/keyboard2.wav")

keyboard2.set_volume(0.2)
keyboard3.set_volume(0.2)

keyboard_sounds = [keyboard2, keyboard3]

clock = pygame.time.Clock()
FPS = 60

SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 600

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

#B = branch, F = finish game, T = toggle, E = entry, L = level
# page name: [button names, action: to which page or toggle a variable or store a text box value, page type]

pages = {'SP2': [['NEXT', 'QUIT', 'ENTER NAME'], ['MM', None, None], ['B', 'F', 'E'], 4],
         'SP1': [['QUIT', 'ENTER NAME'], [None, None], ['F', 'E'], 3],
         'MM': [['START', 'SETTINGS', 'LEADERBOARD', 'QUIT'], ['MSS', 'MO', 'MRS', None], ['B', 'B', 'B', 'F'], 4],
         'MO': [['BACK', 'MUSIC', 'SOUND EFFECTS', 'NAME'], ['MM', True, True, None], ['B', 'T', 'T', 'E'], 5],
         'MRS': [['BACK', 'LVL. 1', 'LVL. 2', 'LVL. 3'], ['MM', None, None, None], ['B', 'L', 'L', 'L'], 4],
         'MRD': [['BACK'], ['MRS'], ['B'], 1],
         'MSS': [['BACK', 'LEVELS', 'TUTORIAL'], ['MM', 'MLS', None], ['B', 'B', 'L'], 3],
         'MLS': [['BACK', 'LVL. 1', 'LVL. 2', 'LVL. 3'], ['MSS', None, None, None], ['B', 'L', 'L', 'L'], 4],}

current_page = 'SP1'

def update_page():
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

def validate_user_input(buttons, database):
    return True

def update_user_input(buttons, current_page, pages_list):
    button_number = buttons.get_chosen_button()
    user_text = buttons.get_list_buttons()[button_number].get_user_text()

    pages_list[current_page][1][button_number] = user_text

    return pages_list

def update_sounds_running(buttons, current_page, sound_effects_running, music_running):
    button_number = buttons.get_chosen_button()
    toggle_value = buttons.get_list_buttons()[button_number].get_toggled()

    if current_page == 'MO':
        if button_number == 1:
            if toggle_value:
                music_running = True
            else:
                music_running = False

        elif button_number == 2:
            if toggle_value:
                sound_effects_running = True
            else:
                sound_effects_running = False

    return sound_effects_running, music_running

def random_keyboard_sound():
    index = random.randint(0, len(keyboard_sounds)-1)
    return keyboard_sounds[index]

run = True
text_box_selected = False
sound_effects_running = True
music_running = True
buttons = update_page()
start_page = True
initial_name_done = False

pygame.mixer.music.play(-1)

while run:

    clock.tick(FPS)

    bg.draw()
    buttons.draw()

    if music_running:
        pygame.mixer.music.set_volume(0.5)
    else:
        pygame.mixer.music.set_volume(0)

    if sound_effects_running:
        keyboard2.set_volume(0.2)
        keyboard3.set_volume(0.2)
        click_sound.set_volume(0.2)
    else:
        keyboard2.set_volume(0)
        keyboard3.set_volume(0)
        click_sound.set_volume(0)


    if not start_page:
        if not text_box_selected:

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
                                click_sound.play()

                                if buttons.get_chosen_button_type() == 'T':
                                    buttons.get_list_buttons()[i].switch_toggled()
                                    pages = update_toggle(buttons, current_page, pages)
                                    sound_effects_running, music_running = update_sounds_running(buttons, current_page, sound_effects_running, music_running)

                                if buttons.get_chosen_button_type() == 'E':
                                    buttons.get_list_buttons()[buttons.get_chosen_button()].selected_text_box()
                                    text_box_selected = True

                                if buttons.get_chosen_button_type() == 'B':
                                    current_page = route_to_next_page(buttons, current_page)
                                    buttons = update_page()
                                    break

                                if buttons.get_chosen_button_type() == 'F':
                                    run = False


                if event.type == pygame.KEYDOWN:
                    random_keyboard_sound().play()
                    if event.key == pygame.K_RETURN:
                        if buttons.get_active_button() != -1:
                            buttons.set_chosen_button(buttons.get_active_button())
                            buttons.set_button_selected(True)
                            click_sound.play()

                            if buttons.get_chosen_button_type() == 'T':
                                buttons.get_list_buttons()[buttons.get_chosen_button()].switch_toggled()
                                pages = update_toggle(buttons, current_page, pages)
                                sound_effects_running, music_running = update_sounds_running(buttons, current_page, sound_effects_running, music_running)

                            if buttons.get_chosen_button_type() == 'E':
                                buttons.get_list_buttons()[buttons.get_chosen_button()].selected_text_box()
                                text_box_selected = True

                            if buttons.get_chosen_button_type() == 'B':
                                current_page = route_to_next_page(buttons, current_page)
                                buttons = update_page()
                                break

                            if buttons.get_chosen_button_type() == 'F':
                                run = False

                    if event.key == pygame.K_SPACE:
                        if buttons.get_active_button() != -1:
                            buttons.set_active_button(buttons.get_active_button() + 1)
                        else:
                            buttons.set_active_button(0)

                    if event.key == pygame.K_ESCAPE:
                        if current_page == 'MM':
                            run = False
                        else:
                            buttons.set_chosen_button(0)
                            current_page = route_to_next_page(buttons, current_page)
                            buttons = update_page()

        else:

            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    run = False

                if event.type == pygame.KEYDOWN:
                    random_keyboard_sound().play()
                    if event.key == pygame.K_BACKSPACE:
                        buttons.get_list_buttons()[buttons.get_chosen_button()].backspace_user_text()
                    elif event.unicode.isprintable() and event.key != pygame.K_SPACE and buttons.get_list_buttons()[buttons.get_chosen_button()].get_len_user_text() < 30:
                        buttons.get_list_buttons()[buttons.get_chosen_button()].add_user_text(event.unicode)
                    elif event.key == pygame.K_RETURN:
                        if validate_user_input(buttons, True):
                            buttons.get_list_buttons()[buttons.get_chosen_button()].unselected_text_box()
                            pages = update_user_input(buttons, current_page, pages)
                            text_box_selected = False

    if start_page:
        if not text_box_selected:

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
                                click_sound.play()

                                if buttons.get_chosen_button_type() == 'E':
                                    buttons.get_list_buttons()[buttons.get_chosen_button()].selected_text_box()
                                    text_box_selected = True

                                if buttons.get_chosen_button_type() == 'B' and initial_name_done:
                                    current_page = route_to_next_page(buttons, current_page)
                                    buttons = update_page()
                                    start_page = False
                                    break

                                if buttons.get_chosen_button_type() == 'F':
                                    run = False

                if event.type == pygame.KEYDOWN:
                    random_keyboard_sound().play()
                    if event.key == pygame.K_RETURN:
                        if buttons.get_active_button() != -1:
                            buttons.set_chosen_button(buttons.get_active_button())
                            buttons.set_button_selected(True)
                            click_sound.play()

                            if buttons.get_chosen_button_type() == 'E':
                                buttons.get_list_buttons()[buttons.get_chosen_button()].selected_text_box()
                                text_box_selected = True

                            if buttons.get_chosen_button_type() == 'B' and initial_name_done:
                                current_page = route_to_next_page(buttons, current_page)
                                buttons = update_page()
                                start_page = False
                                break

                            if buttons.get_chosen_button_type() == 'F':
                                run = False

                    if event.key == pygame.K_SPACE:
                        if buttons.get_active_button() != -1:
                            buttons.set_active_button(buttons.get_active_button() + 1)
                        else:
                            buttons.set_active_button(0)

                    if event.key == pygame.K_ESCAPE:
                        run = False

        else:

            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    run = False

                if event.type == pygame.KEYDOWN:
                    random_keyboard_sound().play()
                    if event.key == pygame.K_BACKSPACE:
                        buttons.get_list_buttons()[buttons.get_chosen_button()].backspace_user_text()
                    elif event.unicode.isprintable() and event.key != pygame.K_SPACE and buttons.get_list_buttons()[
                        buttons.get_chosen_button()].get_len_user_text() < 30:
                        buttons.get_list_buttons()[buttons.get_chosen_button()].add_user_text(event.unicode)
                    elif event.key == pygame.K_RETURN:
                        if validate_user_input(buttons, True):
                            buttons.get_list_buttons()[buttons.get_chosen_button()].unselected_text_box()
                            pages = update_user_input(buttons, current_page, pages)

                            initial_name_done = True
                            pages['SP2'][1][2] = pages['SP1'][1][1]
                            pages['MO'][1][3] = pages['SP1'][1][1]
                            current_page = 'SP2'
                            buttons = update_page()
                            text_box_selected = False

    pygame.display.update()

pygame.quit()