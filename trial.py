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

shadow_image = pygame.transform.scale(
    shadow_image,
    (player_size * 2, player_size)
)

#main

player = pygame.Rect(200, 200, player_size, player_size)
shadow = pygame.Rect(100, 200, player_size, player_size)

speed = 5

# 1 = facing right, -1 = facing left
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

                old_player_pos = player.topleft

                player.x = shadow.x + (player_size * direction)
                player.y = shadow.y

                direction *= -1

                shadow.topleft = old_player_pos

    old_position = player.topleft

    keys = pygame.key.get_pressed()

    if keys[pygame.K_w]:
        player.y -= speed
    if keys[pygame.K_s]:
        player.y += speed
    if keys[pygame.K_a]:
        player.x -= speed
    if keys[pygame.K_d]:
        player.x += speed

    shadow.topleft = old_position

    #drawing
    screen.fill((218, 255, 133))

    if direction == 1:
        screen.blit(
            shadow_image,
            (shadow.x, shadow.y)
        )
        current_player_image = player_image

    else:
        flipped_shadow = pygame.transform.flip(
            shadow_image,
            True,
            False
        )
        screen.blit(
            flipped_shadow,
            (shadow.x - player_size, shadow.y)
        )
        current_player_image = pygame.transform.flip(
            player_image,
            True,
            False
        )

    screen.blit(current_player_image, player)

    pygame.display.update()
    clock.tick(60)

pygame.quit()

