import pygame

pygame.init()
pygame.mixer.init()

# Load the music file (supports .mp3, .wav, and .ogg)
pygame.mixer.music.load("assets/music/elevator_music1.mp3")

pygame.mixer.music.set_volume(0.5)

pygame.mixer.music.play(-1)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False