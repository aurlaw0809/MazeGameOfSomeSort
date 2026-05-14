import pygame
import math
pygame.init()

#---------------------------------------------------------------------------------------------------------------------------------------------------------------
#setup of window

WIDTH, HEIGHT = 800, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))

clock = pygame.time.Clock()

#---------------------------------------------------------------------------------------------------------------------------------------------------------------
#player

player_image = pygame.image.load("goldfish.png").convert_alpha()

player_size = 50

player_image = pygame.transform.scale(
    player_image,
    (player_size, player_size)
)

#---------------------------------------------------------------------------------------------------------------------------------------------------------------
#shadow

shadow_length = 5

shadow_image = pygame.transform.scale(
    player_image.copy(),
    (player_size * shadow_length, player_size)
)

dark_surface = pygame.Surface(
    shadow_image.get_size(),
    pygame.SRCALPHA
)

dark_surface.fill((0, 0, 0, 180))

shadow_image.blit(
    dark_surface,
    (0, 0),
    special_flags=pygame.BLEND_RGBA_SUB
)

#---------------------------------------------------------------------------------------------------------------------------------------------------------------
#main

player = pygame.Rect(200, 200, player_size, player_size)

speed = 5

direction = 0
rotating_clock = False
rotating_aclock = False
running = True

while running:

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_o:
                rotating_clock = True
            if event.key == pygame.K_p:
                rotating_aclock = True

            if event.key == pygame.K_SPACE:
                if direction % 45 == 0:

                    move_vector = pygame.Vector2(1, 0).rotate(direction)
                    distance = player_size * (shadow_length - 1)

                    player.x += move_vector.x * distance
                    player.y += move_vector.y * distance

                    direction = (direction + 180) % 360

        if event.type == pygame.KEYUP:

            if event.key == pygame.K_o or event.key == pygame.K_p:

                rotating_clock = False
                rotating_aclock = False
                direction = round(direction / 45) * 45
                direction %= 360

    keys = pygame.key.get_pressed()

    if keys[pygame.K_w]:
        player.y -= speed
    if keys[pygame.K_s]:
        player.y += speed
    if keys[pygame.K_a]:
        player.x -= speed
    if keys[pygame.K_d]:
        player.x += speed

    if rotating_clock:
        direction += 1
    if rotating_aclock:
        direction -= 1

    shadow_distance = player_size * 2
    offset = pygame.Vector2(shadow_distance, 0)
    rotated_offset = offset.rotate(direction)
    shadow_pos = pygame.Vector2(player.center) + rotated_offset
    '''this bit with vector2 works by finding the vector distance that the shadow would be away
    if it were straight and then rotating it to the actual shadow direction'''

    rotated_shadow = pygame.transform.rotate(
        shadow_image,
        -direction
    )

    shadow_rect = rotated_shadow.get_rect(
        center=shadow_pos
    )

    screen.fill((218, 255, 133))
    screen.blit(rotated_shadow, shadow_rect)
    screen.blit(player_image, player)

    pygame.display.update()
    clock.tick(60)

pygame.quit()