import pygame
pygame.init()

#window
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))

clock = pygame.time.Clock()

#sprites
player_image = pygame.image.load("goldfish.png").convert_alpha()

player_size = 50
player_image = pygame.transform.scale(
    player_image,
    (player_size, player_size)
)

# Create darker shadow version

shadow_length = 5

shadow_image = player_image.copy()

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

shadow_image_east = pygame.transform.scale(
    shadow_image,
    (player_size * shadow_length, player_size)
)

shadow_image_west = pygame.transform.flip(
    shadow_image_east,
    True,
    False)

shadow_image_north = pygame.transform.rotate(
    shadow_image_east,
    90,
)

shadow_image_south = pygame.transform.flip(
    shadow_image_north,
    False,
    True
)

#main

player = pygame.Rect(200, 200, player_size, player_size)
shadow_horiz = pygame.Rect(200, 200, player_size * shadow_length, player_size)
shadow_vert = pygame.Rect(200, 200, player_size, player_size * shadow_length)

speed = 5

# 1 = shadow to the east, 2 = shadow to the south, 3 = shadow to the west, 0 = shadow to the north
direction = 1
running = True

while running:

    #movement
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # space = teleport to end of shadow
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:

                x_mod = 0
                y_mod = 0

                if direction == 1:
                    x_mod = 1
                elif direction == 2:
                    y_mod = 1
                elif direction == 3:
                    x_mod = -1
                elif direction == 0:
                    y_mod = -1

                player.x += (player_size * (shadow_length - 1) * x_mod)
                player.y += (player_size * (shadow_length - 1) * y_mod)

                direction = (direction + 2)% 4
                print(direction)

            elif event.key == pygame.K_t:
                direction = (direction + 1) % 4

    keys = pygame.key.get_pressed()

    if keys[pygame.K_w]:
        player.y -= speed
    if keys[pygame.K_s]:
        player.y += speed
    if keys[pygame.K_a]:
        player.x -= speed
    if keys[pygame.K_d]:
        player.x += speed

    if direction == 1:
        shadow_horiz.topleft = player.topleft
    elif direction == 2:
        shadow_vert.topleft = player.topleft
    elif direction == 3:
        shadow_horiz.bottomright = player.bottomright
    elif direction == 0:
        shadow_vert.bottomright = player.bottomright

    #drawing
    screen.fill((218, 255, 133))

    if direction == 1:
        screen.blit(shadow_image_east, shadow_horiz)
    elif direction == 2:
        screen.blit(shadow_image_south, shadow_vert)
    elif direction == 3:
        screen.blit(shadow_image_west, shadow_horiz)
    elif direction == 0:
        screen.blit(shadow_image_north, shadow_vert)

    screen.blit(player_image, player)

    pygame.display.update()
    clock.tick(60)

pygame.quit()

