import pygame
import math

pygame.init()

clock = pygame.time.Clock()
FPS = 60

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Trialing BG")

sky = pygame.image.load('../assets/skies/sky1/1.png').convert_alpha()

scale_factor = SCREEN_HEIGHT / sky.get_height()

sky = pygame.transform.scale_by(sky, scale_factor)

shoot = pygame.image.load('../assets/skies/sky1/3.png').convert_alpha()
shoot = pygame.transform.scale_by(shoot, scale_factor)

back_cloud = pygame.image.load('../assets/skies/sky1/2.png').convert_alpha()
back_cloud = pygame.transform.scale_by(back_cloud, scale_factor)

middle_cloud = pygame.image.load('../assets/skies/sky1/4.png').convert_alpha()
middle_cloud = pygame.transform.scale_by(middle_cloud, scale_factor)

front_cloud = pygame.image.load('../assets/skies/sky1/5.png').convert_alpha()
front_cloud = pygame.transform.scale_by(front_cloud, scale_factor)

scroll1 = 0
scroll2 = 0
scroll3 = 0

tiles = math.ceil(SCREEN_WIDTH / sky.get_width()) + 1

run =True
while run:

    clock.tick(FPS)

    for a in range(0, tiles):
        screen.blit(sky, (a * sky.get_width() + scroll1, 0))

    for b in range(0, tiles):
        screen.blit(back_cloud, (b * back_cloud.get_width() + scroll1, 0))

    for c in range(0, tiles):
        screen.blit(shoot, (c * front_cloud.get_width() + scroll2, 0))

    for d in range(0, tiles):
        screen.blit(middle_cloud, (d * middle_cloud.get_width() + scroll2, 0))

    for e in range(0, tiles):
        screen.blit(front_cloud, (e * front_cloud.get_width() + scroll3, 0))

    scroll1 -= 0.5
    scroll2 -= 1
    scroll3 -= 2

    if abs(scroll1) > sky.get_width():
        scroll1 = 0

    if abs(scroll2) > sky.get_width():
        scroll2 = 0

    if abs(scroll3) > sky.get_width():
        scroll3 = 0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    pygame.display.update()

pygame.quit()