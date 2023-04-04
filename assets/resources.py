import os

import pygame

from . import globals

data_dir = os.path.split(os.path.abspath(__file__))[0]

def load_image(name, colorkey=None):
    fullname = os.path.join(data_dir, "images", name)
    image = pygame.image.load(fullname)
    if colorkey is not None:
        if colorkey == -1:
            colorkey = image.get_at((0,0))
        image.set_colorkey(colorkey)
    return image, image.get_rect()


def load_font(name, size=2 * globals.WIDTH_UNIT):
    if not pygame.font.get_init():
        pygame.font.init()

    full_name = os.path.join(data_dir, "font", name)
    font = pygame.font.Font(full_name, size)
    return font

class Font:
    def __init__(self):
        self.gameover_font = load_font("bit5x3.ttf", 10 * globals.WIDTH_UNIT)
        self.credit_font = load_font("bit5x3.ttf", 2 * globals.WIDTH_UNIT)
        self.replay_font = load_font("bit5x3.ttf", 5 * globals.WIDTH_UNIT)
        self.score_font = load_font("bit5x3.ttf", 12 * globals.WIDTH_UNIT)
        self.vector_font = load_font("bit5x3.ttf", 3 * globals.WIDTH_UNIT)
        self.player_font = load_font("bit5x3.ttf", 3 * globals.WIDTH_UNIT)
