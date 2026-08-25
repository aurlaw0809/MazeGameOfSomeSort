import pygame
import math

pygame.init()

clock = pygame.time.Clock()
FPS = 60

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Trialing slider")

#test_grid = pygame.image.load('assets/test_square.png').convert()
#test_grid = pygame.transform.scale(test_grid, (SCREEN_WIDTH, SCREEN_HEIGHT))

TRACK_WIDTH = 600
TRACK_HEIGHT = 400
TRACK_THICKNESS = 10

TRACK_CORNER_R = 100
TRACK_CORNER_D = 100

TRACK_CENTER = (TRACK_CORNER_R + TRACK_WIDTH / 2,
                TRACK_CORNER_D + TRACK_HEIGHT / 2)

top_bar = pygame.Rect(TRACK_CORNER_R - TRACK_THICKNESS / 2,
                      TRACK_CORNER_D - TRACK_THICKNESS / 2,
                      TRACK_WIDTH + TRACK_THICKNESS,
                      TRACK_THICKNESS)

left_bar = pygame.Rect(TRACK_CORNER_R - TRACK_THICKNESS / 2,
                       TRACK_CORNER_D - TRACK_THICKNESS / 2,
                       TRACK_THICKNESS,
                       TRACK_HEIGHT)

right_bar = pygame.Rect(TRACK_CORNER_R + TRACK_WIDTH - TRACK_THICKNESS / 2,
                        TRACK_CORNER_D - TRACK_THICKNESS / 2,
                        TRACK_THICKNESS,
                        TRACK_HEIGHT)

bottom_bar = pygame.Rect(TRACK_CORNER_R - TRACK_THICKNESS / 2,
                        TRACK_CORNER_D + TRACK_HEIGHT - TRACK_THICKNESS / 2,
                         TRACK_WIDTH + TRACK_THICKNESS,
                         TRACK_THICKNESS)

#center_test = pygame.Rect(TRACK_CENTER[0], TRACK_CENTER[1], 10, 10)

SLIDER_WIDTH = 20
SLIDER_HEIGHT = 20

active_slider = False

max_x = TRACK_CORNER_R + TRACK_WIDTH - SLIDER_WIDTH / 2
min_x = TRACK_CORNER_R - SLIDER_WIDTH / 2
max_y = TRACK_CORNER_D + TRACK_HEIGHT - SLIDER_HEIGHT / 2
min_y = TRACK_CORNER_D - SLIDER_HEIGHT / 2

slider = pygame.Rect(min_x + TRACK_WIDTH / 2,
                     min_y,
                     SLIDER_WIDTH,
                     SLIDER_HEIGHT)

def check_valid_pos(pos):
    #left and right bar
    if pos[0] == min_x or pos[0] == max_x:
        if max_y >= pos[1] >= min_y:
            return True
        else:
            return False
    #top and bottom bar
    elif pos[1] == min_y or pos[1] == max_y:
        if max_x >= pos[0] >= min_x:
            return True
        else:
            return False
    else:
        return False

def pos_from_keys(adder, pos):
    if pos[0] > min_x:
        new_pos = (pos[0], pos[1] + adder)
    else:
        new_pos = (pos[0], pos[1] - adder)

    if check_valid_pos(new_pos):
        pos = new_pos
    else:
        new_pos = pos

    if pos[1] > min_y:
        new_pos = (pos[0] - adder, pos[1])
    else:
        new_pos = (pos[0] + adder, pos[1])

    if check_valid_pos(new_pos):
        pos = new_pos
    else:
        new_pos = pos

    return pos

def calculate_angle(pos):

    dx = pos[0] + SLIDER_WIDTH / 2 - TRACK_CENTER[0]
    dy = pos[1] + SLIDER_HEIGHT / 2 - TRACK_CENTER[1]

    angle = math.degrees(math.atan2(dy, dx))
    angle %= 360
    angle = round(angle)

    return angle

clockwise = False
anticlockwise = False

angle = 0

run = True
while run:

    screen.fill((219, 227, 127))

    #screen.blit(test_grid, (0, 0))

    pygame.draw.rect(screen, (120, 176, 69), top_bar)
    pygame.draw.rect(screen, (120, 176, 69), left_bar)
    pygame.draw.rect(screen, (120, 176, 69), right_bar)
    pygame.draw.rect(screen, (120, 176, 69), bottom_bar)

    #pygame.draw.rect(screen, (120, 176, 69), center_test)

    pygame.draw.rect(screen, (255, 255, 255), slider)

    angle = calculate_angle((slider.x, slider.y))

    font = pygame.font.Font(None, 36)
    text = font.render(f"Angle: {angle}", True, (120, 176, 69))
    screen.blit(text, (20, 20))

    if anticlockwise:
        new_pos = pos_from_keys(-1, (slider.x, slider.y))
        slider.x = new_pos[0]
        slider.y = new_pos[1]

    if clockwise:
        new_pos = pos_from_keys(1, (slider.x, slider.y))
        slider.x = new_pos[0]
        slider.y = new_pos[1]

    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                if slider.collidepoint(event.pos):
                    active_slider = True

        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                active_slider = False

        if event.type == pygame.MOUSEMOTION:
            if active_slider:
                new_pos = (slider.x + event.rel[0], slider.y + event.rel[1])
                if check_valid_pos(new_pos):
                    slider.move_ip(event.rel)

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_o:
                anticlockwise = True
            if event.key == pygame.K_p:
                clockwise = True

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_o:
                anticlockwise = False
            if event.key == pygame.K_p:
                clockwise = False

        if event.type == pygame.QUIT:
            run = False

    pygame.display.flip()

pygame.quit()