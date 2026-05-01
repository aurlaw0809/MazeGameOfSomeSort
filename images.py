from pygame.image import load
from pygame.math import Vector2

def load_sprite(name, with_alpha=True):
    path = f"{name}.png"
    loaded_sprite = load(path)
    #loaded_sprite = pygame.transform.scale(loaded_sprite, (800, 600))

    if with_alpha:
        return loaded_sprite.convert_alpha()
    else:
        return loaded_sprite.convert()

def wrap_position(position, surface):
    x, y = position
    w, h = surface.get_size()
    return Vector2(x % w, y % h)