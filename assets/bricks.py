import pygame
from . import globals
from random import randint

class Brick(pygame.sprite.Sprite):
    def __init__(self, color=globals.WHITE, x=0, y=0):
        super().__init__()
        self.image = pygame.Surface([globals.BRICK_WIDTH, globals.BRICK_HEIGHT])
        self.color = color
        self.image.fill(self.color)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.width = globals.BRICK_WIDTH
        self.height = globals.BRICK_HEIGHT
        
    def draw(self, screen):
        pygame.draw.rect(screen, self.color, [self.rect.x, self.rect.y, self.width, self.height])

    def pop():
        pass

class BricksLayers:
    def __init__(self, x=7, y=120, layers = globals.NUMLAYERS):
        self.bricks = []
        for i in range(2 * int(globals.WINDOW_WIDTH / (globals.BRICK_WIDTH + globals.BRICK_X_GAP))):
            for j in range(layers):
                # Create a random color
                color = '#%06X' % randint(0, 0xFFFFFF)
                # Add a brick to list
                self.bricks.append(Brick(color, x + i * globals.BRICK_X_GAP, y - j * globals.BRICK_HEIGHT - j * globals.BRICKS_Y_GAP))