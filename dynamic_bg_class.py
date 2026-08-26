import pygame
import math

class DynamicBackground():
    def __init__(self, screen):
        self.screen = screen
        self.screen_width = screen.get_width()
        self.screen_height = screen.get_height()

        self.sky = pygame.image.load('assets/skies/1.png').convert_alpha()

        scale_factor = self.screen_height / self.sky.get_height()

        self.sky = pygame.transform.scale_by(self.sky, scale_factor)

        self.shoot = pygame.image.load('assets/skies/2.png').convert_alpha()
        self.shoot = pygame.transform.scale_by(self.shoot, scale_factor)

        self.back_cloud = pygame.image.load('assets/skies/3.png').convert_alpha()
        self.back_cloud = pygame.transform.scale_by(self.back_cloud, scale_factor)

        self.middle_cloud = pygame.image.load('assets/skies/4.png').convert_alpha()
        self.middle_cloud = pygame.transform.scale_by(self.middle_cloud, scale_factor)

        self.front_cloud = pygame.image.load('assets/skies/5.png').convert_alpha()
        self.front_cloud = pygame.transform.scale_by(self.front_cloud, scale_factor)

        self.scroll1 = 0
        self.scroll2 = 0
        self.scroll3 = 0

        self.tiles = math.ceil(self.screen_width / self.sky.get_width()) + 1

    def draw(self):

        for a in range(0, self.tiles):
            self.screen.blit(self.sky, (a * self.sky.get_width() + self.scroll1, 0))

        for b in range(0, self.tiles):
            self.screen.blit(self.back_cloud, (b * self.back_cloud.get_width() + self.scroll1, 0))

        for c in range(0, self.tiles):
            self.screen.blit(self.shoot, (c * self.front_cloud.get_width() + self.scroll2, 0))

        for d in range(0, self.tiles):
            self.screen.blit(self.middle_cloud, (d * self.middle_cloud.get_width() + self.scroll2, 0))

        for e in range(0, self.tiles):
            self.screen.blit(self.front_cloud, (e * self.front_cloud.get_width() + self.scroll3, 0))

        self.scroll1 -= 0.5
        self.scroll2 -= 1
        self.scroll3 -= 2

        if abs(self.scroll1) > self.sky.get_width():
            self.scroll1 = 0

        if abs(self.scroll2) > self.sky.get_width():
            self.scroll2 = 0

        if abs(self.scroll3) > self.sky.get_width():
            self.scroll3 = 0