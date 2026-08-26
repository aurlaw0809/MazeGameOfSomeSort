import pygame

class TextBox():
    def __init__(self, screen, x, y,
                 width, height,
                 inactive_color, active_colour,
                 text_color, text_font, text_x, text_y):

        self.screen = screen
        self.x = x
        self.y = y

        self.width = width
        self.height = height

        self.inactive_color = inactive_color
        self.active_colour = active_colour
        self.colour = self.inactive_color

        self.text_color = text_color
        self.text_font = text_font
        self.text_x = text_x
        self.text_y = text_y
        self.text = ''

        self.selected = False
        self.valid = False

    def update_colour(self):
        if self.selected:
            self.colour = self.active_colour
        else:
            self.colour = self.inactive_color

    def make_active(self):
        self.selected = True
        self.update_colour()

    def make_inactive(self):
        self.selected = False
        self.update_colour()

    def is_active(self):
        return self.selected

    def draw(self):
        surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        surface.fill(self.colour)
        self.screen.blit(surface, (self.x, self.y))

        text = self.text_font.render(f"{self.text}", True, self.text_color)
        self.screen.blit(text, (self.x + self.text_x, self.y + self.text_y))