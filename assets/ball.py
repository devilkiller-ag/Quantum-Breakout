import random

import pygame

from . import globals

class Ball(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        self.image = pygame.Surface([globals.WIDTH_UNIT, globals.WIDTH_UNIT])
        self.image.fill(globals.WHITE)
        self.rect = self.image.get_rect()
        self.velocity = [1,2]
        self.initial_speed = 2
        self.reset(direction=1)

    def update(self, classical_computer, quantum_computer):
        self.rect.x += self.velocity[0]
        self.rect.y += self.velocity[1]

        if self.rect.y < 0 or self.rect.y > globals.FIELD_HEIGHT - globals.WIDTH_UNIT:
            self.velocity[1] = -self.velocity[1]
        
        if self.rect.x < 0:
            self.reset(1)
            quantum_computer.score += 1
        elif self.rect.x > globals.WINDOW_WIDTH:
            self.reset(-1)
            classical_computer.score += 1

    def bounce(self):
        # ball is sped up 50% after each bounce
        self.velocity[0] = -self.velocity[0] * 1.5
        self.velocity[1] = self.velocity[1] * 1.5      

    def reset(self, direction):
        self.rect.centerx = globals.WINDOW_WIDTH / 2
        self.rect.centery = globals.FIELD_HEIGHT / 2

        if direction > 0:
            self.velocity = [random.randint(2,4), random.randint(-4,4)] * self.initial_speed
        else:
            self.velocity = [random.randint(-4,-2), random.randint(-4,4)] * self.initial_speed