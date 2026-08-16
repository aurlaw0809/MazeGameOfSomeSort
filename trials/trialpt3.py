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

#main

player = pygame.Rect(200, 200, player_size, player_size)
shadow = pygame.Rect(200, 200, player_size * shadow_length, player_size)

speed = 5

# 1 = e, 1.5 = se, 2 = s, 2.5 = sw,3 = w, 3.5 = nw, 0 = n, 0.5 = ne
#TODO convert directions instead of numbers to angles would be great
direction = 1
running = True

def rotate_pivot(surface, angle, pivot, offset):
    rotated_image = pygame.transform.rotate(surface, angle)
    rotated_offset = offset.rotate(-angle)
    rect = rotated_image.get_rect(center=pivot + rotated_offset)
    return rotated_image, rect

while running:

    old_direction = direction
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

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_t:
                direction %= 4

    keys = pygame.key.get_pressed()

    if keys[pygame.K_w]:
        player.y -= speed
    if keys[pygame.K_s]:
        player.y += speed
    if keys[pygame.K_a]:
        player.x -= speed
    if keys[pygame.K_d]:
        player.x += speed

    if keys[pygame.K_t]:
        direction += .1

    angle = (old_direction - direction) * 90
    shadow = rotate_pivot(shadow, angle, player.centre, player_size * (shadow_length - .5))

    #drawing
    screen.fill((218, 255, 133))

    screen.blit(shadow_image, shadow)
    screen.blit(player_image, player)

    pygame.display.update()
    clock.tick(60)

pygame.quit()

