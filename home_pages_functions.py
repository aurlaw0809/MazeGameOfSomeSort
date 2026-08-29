import sqlite3
from db_commands import *
import random

def random_keyboard_sound(keyboard_sounds):
    index = random.randint(0, len(keyboard_sounds)-1)
    return keyboard_sounds[index]

def route_to_next_page(buttons, current_page, pages):
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

def validate_user_name_input(user_name):

    return name_entered(user_name)