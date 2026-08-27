import pygame
import time
import random

pygame.init()

clock = pygame.time.Clock()
FPS = 60

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

class Button:
    def __init__(self, x, y, width, height, inactive_color, active_colour, text, text_color, text_font, text_x, text_y):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

        self.inactive_color = inactive_color
        self.active_colour = active_colour
        self.active = False

        self.text = text
        self.text_color = text_color
        self.text_font = text_font
        self.text_x = text_x
        self.text_y = text_y

        self.colour = self.inactive_color

    def update_colour(self):
        if self.active:
            self.colour = self.active_colour
        else:
            self.colour = self.inactive_color

    def draw(self):
        pygame.draw.rect(screen, self.colour, (self.x, self.y, self.width, self.height))
        text = self.text_font.render(f"{self.text}", True, self.text_color)
        screen.blit(text, (self.x + self.text_x, self.y + self.text_y))

    def make_active(self):
        self.active = True
        self.update_colour()

    def make_inactive(self):
        self.active = False
        self.update_colour()

    def check_collision(self, pos):
        if pygame.Rect(self.x, self.y, self.width, self.height).collidepoint(pos):
            self.make_active()
            return True
        else:
            self.make_inactive()
            return False

    def is_active(self):
        return self.active

BG_COLOR = (219, 227, 127)

TEXT_COLOR = (255, 255, 255)
TEXT_FONT = pygame.font.SysFont('comicsans', 30)

TEXT_X = 10
TEXT_Y = 5

BUTTON_COLOR = (204, 111, 61)
BUTTON_ACTIVE_COLOR = (224, 176, 92)

BUTTON_WIDTH = 200
BUTTON_HEIGHT = 50

BUTTON_X = 200
BUTTON_Y = 200

BUTTON_SPACING = 25

NUMBER_OF_BUTTONS = 4
LIST_OF_BUTTON_NAMES = ['button 0', 'button 1', 'button 2', 'button 3']
LIST_OF_BUTTONS = []

active_button = -1
chosen_button = -1

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Trialing hover button")

for i in range(NUMBER_OF_BUTTONS):
    LIST_OF_BUTTONS.append(Button(BUTTON_X,
                                  BUTTON_Y + (BUTTON_HEIGHT + BUTTON_SPACING) * i,
                                  BUTTON_WIDTH,
                                  BUTTON_HEIGHT,
                                  BUTTON_COLOR,
                                  BUTTON_ACTIVE_COLOR,
                                  LIST_OF_BUTTON_NAMES[i],
                                  TEXT_COLOR,
                                  TEXT_FONT,
                                  TEXT_X,
                                  TEXT_Y))

button_selected = False

def print_button_selected(i):
    text = TEXT_FONT.render(f"SELECTED: {LIST_OF_BUTTON_NAMES[i]}", True, TEXT_COLOR)
    screen.blit(text, (20, 20))

def print_button_active(i):
    text = TEXT_FONT.render(f"ACTIVE: {LIST_OF_BUTTON_NAMES[i]}", True, TEXT_COLOR)
    screen.blit(text, (20, 50))

run = True
while run:

    clock.tick(FPS)

    screen.fill(BG_COLOR)

    print_button_active(active_button)

    if button_selected:
        print_button_selected(chosen_button)

    for i in range(0, len(LIST_OF_BUTTONS)):
        if active_button == i:
            LIST_OF_BUTTONS[i].make_active()
        else:
            LIST_OF_BUTTONS[i].make_inactive()
        LIST_OF_BUTTONS[i].draw()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
        if event.type == pygame.MOUSEMOTION:
            i = 0
            for i in range(0, len(LIST_OF_BUTTONS)):
                if LIST_OF_BUTTONS[i].check_collision(event.pos):
                    active_button = i

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                i = 0
                for i in range(0, len(LIST_OF_BUTTONS)):
                    if LIST_OF_BUTTONS[i].check_collision(event.pos):
                        active_button = i
                    if LIST_OF_BUTTONS[i].is_active():
                        button_selected = True
                        chosen_button = i

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                if active_button != -1:
                    chosen_button = active_button
                    button_selected = True

            if event.key == pygame.K_SPACE:
                if active_button != -1:
                    active_button += 1
                    active_button %= 4
                else:
                    active_button = 0


    pygame.display.flip()

pygame.quit()