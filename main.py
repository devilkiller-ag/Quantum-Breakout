# Import files and libraries
import pygame
from assets import globals, scene

# Initialise pygame and create window
pygame.init()
screen = pygame.display.set_mode((globals.WINDOW_WIDTH, globals.WINDOW_HEIGHT))
pygame.display.set_caption('Quantum Breakout')
clock = pygame.time.Clock()


def main():
    # initialize game
    scene_manager = scene.SceneManager()
    scene_manager.push(scene.GameScene())

    while not scene_manager.exit:
        # update game
        scene_manager.update()
        # draw game
        scene_manager.draw(screen)
        # control framerate
        clock.tick(60)

if __name__ == '__main__':
    main()