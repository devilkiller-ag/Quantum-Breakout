import pygame

from assets.circuit_grid import CircuitGrid
from assets import globals, ui, paddle, ball, computer, resources

class Scene:
    def __init__(self) -> None:
        pass
    def update(self, sm):
        pass
    def draw(self, sm, screen):
        pass

class SceneManager:
    def __init__(self) -> None:
        self.scenes = []
        self.exit = False
    def update(self):
        if len(self.scenes) > 0:
            self.scenes[-1].update(self)
    def draw(self, screen):
        screen.fill(globals.BLACK)
        if len(self.scenes) > 0:
            self.scenes[-1].draw(self, screen)
        pygame.display.flip()
    def push(self, scene):
        self.scenes.append(scene)

class GameScene(Scene):
    def __init__(self) -> None:
        super().__init__()
        self.circuit_grid = CircuitGrid(5, globals.FIELD_HEIGHT)
        self.quantum_paddles = paddle.QuantumPaddles(globals.STATEVECTOR_WIDTH)
        self.quantum_computer = computer.QuantumComputer(self.quantum_paddles, self.circuit_grid)
        self.pong_ball = ball.Ball()
        self.moving_sprites = pygame.sprite.Group()
        self.moving_sprites.add(self.quantum_paddles.paddles)
        self.moving_sprites.add(self.pong_ball)
    
    def update(self, sm):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sm.exit = True
            elif event.type == pygame.KEYDOWN:
                self.circuit_grid.handle_input(event.key)

        self.pong_ball.update(self.quantum_computer)
        self.quantum_computer.update(self.pong_ball)

        if self.quantum_computer.score >= globals.WIN_SCORE:
            sm.push(WinScene())

    def draw(self, sm, screen):
        self.circuit_grid.draw(screen)
        ui.draw_statevector_grid(screen)
        ui.draw_score(screen, self.quantum_computer.score)
        self.moving_sprites.draw(screen)

class LoseScene(Scene):
    def __init__(self) -> None:
        super().__init__()

    def update(self, sm):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sm.exit = True
            elif event.type == pygame.KEYDOWN:
                # press SPACE to reply
                if event.key == pygame.K_SPACE:
                    sm.push(GameScene())

    def draw(self, sm, screen):
        font = resources.Font()

        gameover_text = "Game Over"
        text = font.gameover_font.render(gameover_text, 1, globals.WHITE)
        text_pos = text.get_rect(center=(globals.WINDOW_WIDTH/2, globals.WIDTH_UNIT*20))
        screen.blit(text, text_pos)

        gameover_text = "Press Space to Replay!"
        text = font.replay_font.render(gameover_text, 5, globals.WHITE)
        text_pos = text.get_rect(center=(globals.WINDOW_WIDTH/2, globals.WIDTH_UNIT*30))
        screen.blit(text, text_pos)

class WinScene(Scene):
    def __init__(self) -> None:
        super().__init__()

    def update(self, sm):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sm.exit = True
            elif event.type == pygame.KEYDOWN:
                # press SPACE to reply
                if event.key == pygame.K_SPACE:
                    sm.push(GameScene())

    def draw(self, sm, screen):
        font = resources.Font()

        gameover_text = "Congratulations!"
        text = font.gameover_font.render(gameover_text, 5, globals.WHITE)
        text_pos = text.get_rect(center=(globals.WINDOW_WIDTH/2, globals.WIDTH_UNIT*20))
        screen.blit(text, text_pos)

        gameover_text = "You demonstrated quantum advantage"
        text = font.replay_font.render(gameover_text, 5, globals.WHITE)
        text_pos = text.get_rect(center=(globals.WINDOW_WIDTH/2, globals.WIDTH_UNIT*30))
        screen.blit(text, text_pos)

        gameover_text = "Press Space to Replay!"
        text = font.replay_font.render(gameover_text, 5, globals.WHITE)
        text_pos = text.get_rect(center=(globals.WINDOW_WIDTH/2, globals.WIDTH_UNIT*35))
        screen.blit(text, text_pos)
