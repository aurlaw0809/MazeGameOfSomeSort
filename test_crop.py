import pygame
import math

pygame.init()

clock = pygame.time.Clock()
FPS = 60

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Trialing BG")

screen.fill((120, 176, 69))

image = pygame.image.load('assets/starchy/S0.png')
image = pygame.transform.scale(image, (50, image.get_height() / image.get_width() * 50))

cropped = pygame.Surface((20, 20))


run =True
while run:

    clock.tick(FPS)

    screen.blit(image, (100, 100))
    screen.blit(image, (200, 200), (20, 20, 50, 50))
    #screen.blit(picture you want to blit, (pos to blit to),
    # (pos image starts in (0, 0 from corner or 10, 10 from corner whatever), size of rectangle blitting it to)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    pygame.display.update()

pygame.quit()