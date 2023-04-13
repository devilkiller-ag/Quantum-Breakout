import random

import pygame

from . import globals

class Ball(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.ball_size = globals.BALL_SIZE
        self.image = pygame.Surface([self.ball_size, self.ball_size])
        self.image.fill(globals.WHITE)
        self.rect = self.image.get_rect()
        self.initial_speed = 2
        self.velocity = [1,2] * self.initial_speed
        self.reset()

    def update(self, quantum_computer):
        # Update position of ball
        self.rect.x += self.velocity[0]
        self.rect.y += self.velocity[1]

        # If ball reaches top of the screen: reverse the ball direction
        if self.rect.y < 0:
            self.velocity[1] = -self.velocity[1]

        # If ball reaches leftmost or rightmost wall of the screen: reverse the ball direction
        if self.rect.x < 0 or self.rect.x > globals.WINDOW_WIDTH - self.ball_size:
            self.velocity[0] = -self.velocity[0]
        
        # Reset the ball if it gets out of the screen
        if self.rect.y > globals.FIELD_HEIGHT + self.ball_size:
            self.reset()
            # Increase the no. of ball dropped
            globals.ball_dropped += 1

    def bounce(self):
        # If you want to sped up ball after each bounce: change the percentage_speed_up {[0,1)}
        percentage_speed_up = 0
        self.velocity[0] = self.velocity[0] * (1 + percentage_speed_up)
        self.velocity[1] = -self.velocity[1] * (1 + percentage_speed_up)

    def reset(self):
        self.rect.centerx = globals.PADDLE_WIDTH / 2
        self.rect.centery = globals.WINDOW_HEIGHT * 0.59
        
        # Always go upward when game starts/restarts
        self.velocity = [-1, -2] * self.initial_speed