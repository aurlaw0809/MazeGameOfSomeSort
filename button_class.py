import pygame

class ButtonList:
    def __init__(self, screen, x, y,
                 width, height, spacing,
                 number_buttons, list_names,
                 inactive_color, active_colour,
                 text_color, text_font, text_x, text_y):

        self.screen = screen
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.spacing = spacing

        self.active_button = -1
        self.chosen_button = -1
        self.button_selected = False

        self.number_buttons = number_buttons
        self.list_buttons = []
        self.list_names = list_names

        self.inactive_color = inactive_color
        self.active_colour = active_colour
        self.active = False

        self.text_color = text_color
        self.text_font = text_font
        self.text_x = text_x
        self.text_y = text_y

        self.colour = self.inactive_color

        self.create_buttons()

    def create_buttons(self):
        for i in range(0, self.number_buttons):
            self.list_buttons.append(Button(self.screen,
                                            self.x,
                                            self.y + (self.height + self.spacing) * i,
                                            self.width,
                                            self.height,
                                            self.inactive_color,
                                            self.active_colour,
                                            self.list_names[i],
                                            self.text_color,
                                            self.text_font,
                                            self.text_x,
                                            self.text_y))

    def print_button_selected(self, i):
        text = self.text_font.render(f"SELECTED: {self.list_names[i]}", True, self.text_color)
        self.screen.blit(text, (20, 20))

    def print_button_active(self, i):
        text = self.text_font.render(f"ACTIVE: {self.list_names[i]}", True, self.text_color)
        self.screen.blit(text, (20, 50))

    def draw(self):
        self.print_button_active(self.active_button)

        if self.button_selected:
            self.print_button_selected(self.chosen_button)

        for i in range(0, self.number_buttons):
            if self.active_button == i:
                self.list_buttons[i].make_active()
            else:
                self.list_buttons[i].make_inactive()
            self.list_buttons[i].draw()

    def set_active_button(self, i):
        self.active_button = i
        self.active_button %= self.number_buttons

    def set_button_selected(self, i):
        self.button_selected = i

    def set_chosen_button(self, i):
        self.chosen_button = i

    def get_active_button(self):
        return self.active_button

    def get_button_selected(self):
        return self.button_selected

    def get_chosen_button(self):
        return self.chosen_button

    def get_number_buttons(self):
        return self.number_buttons

    def get_list_buttons(self):
        return self.list_buttons


class Button:
    def __init__(self, screen, x, y,
                 width, height,
                 inactive_color, active_colour,
                 text, text_color, text_font, text_x, text_y):

        self.screen = screen
        self.x = x
        self.y = y
        self.width = width
        self.height = height

        self.inactive_color = inactive_color
        self.active_colour = active_colour
        self.active = False

        self.text = text
        self.text_color = text_color
        self.text_font = text_font
        self.text_x = text_x
        self.text_y = text_y

        self.colour = self.inactive_color

    def update_colour(self):
        if self.active:
            self.colour = self.active_colour
        else:
            self.colour = self.inactive_color

    def draw(self):
        #pygame.draw.rect(self.screen, self.colour, (self.x, self.y, self.width, self.height))

        surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        surface.fill(self.colour)
        self.screen.blit(surface, (self.x, self.y))

        text = self.text_font.render(f"{self.text}", True, self.text_color)
        self.screen.blit(text, (self.x + self.text_x, self.y + self.text_y))

    def make_active(self):
        self.active = True
        self.update_colour()

    def make_inactive(self):
        self.active = False
        self.update_colour()

    def check_collision(self, pos):
        if pygame.Rect(self.x, self.y, self.width, self.height).collidepoint(pos):
            self.make_active()
            return True
        else:
            self.make_inactive()
            return False

    def is_active(self):
        return self.active