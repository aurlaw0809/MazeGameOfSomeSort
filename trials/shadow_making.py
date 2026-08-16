import math
import numpy as np
import pygame

def shadow_image(image, size, colour):

    new_image = pygame.Surface((size, size), pygame.SRCALPHA)
    for y in range(size):
        for x in range(size):
            pixel = image.get_at((x, y))
            if pixel.a == 0:
                continue

            new_image.set_at((x, y), colour)

    return new_image


def shear_image(image, offset):
    width, height = image.get_size()

    new_width = width + abs(offset)
    result = pygame.Surface((new_width, height), pygame.SRCALPHA)

    for y in range(height):
        x_offset = int(offset * (height - 1 - y) / (height - 1))

        if offset < 0:
            x_offset += abs(offset)

        for x in range(width):
            pixel = image.get_at((x, y))
            result.set_at((x + x_offset, y), pixel)

    return result

def shear_and_extend(image, angle, size, height, colour):

    move_vector = pygame.Vector2(height*size, 0).rotate(angle)
    image = shadow_image(image, size, colour)
    image = pygame.transform.smoothscale(image, (size, abs(move_vector.y)))

    offset = move_vector.x
    image = shear_image(image, offset)

    corner_x = 0
    corner_y = 0
    
    if angle >=270 and angle <=360 or angle >= 0 and angle <= 90:
        corner_x = self.player.pos[0] - self.player.get_size() / 2
    else:
        corner_x = self.player.pos[0] - self.player.get_size() / 2 + offset
        
    if angle >= 0 and angle <= 180:
        corner_y = self.player.pos[1] + self.player.get_size() / 2
        image = pygame.transform.flip(image, False, True)
    else:
        corner_y = self.player.pos[1] + self.player.get_size() / 2 - move_vector.y
    


    """
    new_width = move_vector.x * 2 + size
    image = pygame.transform.smoothscale(image, (size, move_vector.y))
    shadow_surface = pygame.Surface((new_width, move_vector.y * 2), flags=pygame.SRCALPHA)

    centre_x = new_width // 2
    centre_y = move_vector.y

    if move_vector.y == 0:
        return None
    else:
        for y in range(int(abs(move_vector.y))):
            offset = 0

            if move_vector.x != 0:
                offset = y * move_vector.x / move_vector.y

            for x in range(size):
                pixel = image.get_at((x, y))
                if pixel.a == 0:
                    continue

                shadow_surface.set_at((centre_x - size / 2 + x + offset, centre_y - move_vector.y + y), colour)
    

    shadow_surface = pygame.transform.scale(shadow_surface, (new_width, move_vector.y))

    return shadow_surface
    """


