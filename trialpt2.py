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
#shadow_image = pygame.image.load("circle_shaodow_maybe.png").convert_alpha()

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

diagonal_size = (0.5*((player_size*shadow_length)**2))**.5

shadow_image_diagonal = pygame.transform.scale(
    shadow_image,
    (diagonal_size, diagonal_size)
)

shadow_image_ne = pygame.transform.rotate(
    shadow_image_diagonal,
    -45
)

shadow_image_se = pygame.transform.flip(
    shadow_image_ne,
    False,
    True
)

shadow_image_sw = pygame.transform.flip(
    shadow_image_se,
    True,
    False
)

shadow_image_nw = pygame.transform.flip(
    shadow_image_ne,
    True,
    False
)

#main

player = pygame.Rect(200, 200, player_size, player_size)
shadow_horiz = pygame.Rect(200, 200, player_size * shadow_length, player_size)
shadow_vert = pygame.Rect(200, 200, player_size, player_size * shadow_length)
shadow_diagonal = pygame.Rect(200, 200, diagonal_size, diagonal_size)

speed = 5

# 1 = e, 1.5 = se, 2 = s, 2.5 = sw,3 = w, 3.5 = nw, 0 = n, 0.5 = ne
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
                d_mod = 0.5**0.5

                if direction == 1:
                    x_mod = 1
                elif direction == 1.5:
                    x_mod = d_mod
                    y_mod = d_mod
                elif direction == 2:
                    y_mod = 1
                elif direction == 2.5:
                    x_mod = -d_mod
                    y_mod = d_mod
                elif direction == 3:
                    x_mod = -1
                elif direction == 3.5:
                    x_mod = -d_mod
                    y_mod = -d_mod
                elif direction == 0:
                    y_mod = -1
                elif direction == 0.5:
                    x_mod = d_mod
                    y_mod = -d_mod

                player.x += (player_size * (shadow_length - 1) * x_mod)
                player.y += (player_size * (shadow_length - 1) * y_mod)

                direction = (direction + 2)% 4
                print(direction)

            elif event.key == pygame.K_t:
                direction = (direction + .5) % 4

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
    if direction == 1.5:
        shadow_diagonal.topleft = player.topleft
    elif direction == 2:
        shadow_vert.topleft = player.topleft
    elif direction == 2.5:
        shadow_diagonal.topright = player.topright
    elif direction == 3:
        shadow_horiz.bottomright = player.bottomright
    elif direction == 3.5:
        shadow_diagonal.bottomright = player.bottomright
    elif direction == 0:
        shadow_vert.bottomright = player.bottomright
    elif direction == 0.5:
        shadow_diagonal.bottomleft = player.bottomleft

    #drawing
    screen.fill((218, 255, 133))

    if direction == 1:
        screen.blit(shadow_image_east, shadow_horiz)
    elif direction == 1.5:
        screen.blit(shadow_image_se, shadow_diagonal)
    elif direction == 2:
        screen.blit(shadow_image_south, shadow_vert)
    elif direction == 2.5:
        screen.blit(shadow_image_sw, shadow_diagonal)
    elif direction == 3:
        screen.blit(shadow_image_west, shadow_horiz)
    elif direction == 3.5:
        screen.blit(shadow_image_nw, shadow_diagonal)
    elif direction == 0:
        screen.blit(shadow_image_north, shadow_vert)
    elif direction == 0.5:
        screen.blit(shadow_image_ne, shadow_diagonal)

    screen.blit(player_image, player)

    pygame.display.update()
    clock.tick(60)

pygame.quit()

