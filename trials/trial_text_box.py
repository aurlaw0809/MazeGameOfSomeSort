import pygame

pygame.init()

clock = pygame.time.Clock()
FPS = 60

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Trialing text box")

font = pygame.font.Font('../assets/fonts/pressstart2p.ttf', 30)
user_text = ''

run = True
while run:

    clock.tick(FPS)

    screen.fill((219, 227, 127))

    text_surface = font.render(user_text, True, (255, 255, 255))
    screen.blit(text_surface, (50, 50))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE:
                user_text = user_text[:-1]
            elif event.unicode.isprintable() and event.key != pygame.K_SPACE and len(user_text) < 20:
                user_text += event.unicode

    pygame.display.flip()

pygame.quit()