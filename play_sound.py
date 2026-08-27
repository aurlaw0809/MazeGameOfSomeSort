import pygame
import time

pygame.init()
pygame.mixer.init()

# Load the music file (supports .mp3, .wav, and .ogg)
sound = pygame.mixer.Sound("assets/sound_effects/keyboard3.wav")

sound.set_volume(0.5)

running = True
while running:
    sound.play()
    time.sleep(1)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            sound.play()