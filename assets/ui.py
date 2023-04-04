import pygame

from . import globals, resources

def draw_statevector_grid(screen):
    font = resources.Font()
    
    basis_states = globals.BASIS_STATES
    statevector_width = globals.STATEVECTOR_WIDTH
    statevector_height = globals.STATEVECTOR_HEIGHT

    for i in range(len(basis_states)):
        text = font.vector_font.render(basis_states[i], 1, globals.WHITE)
        screen.blit(text, (i*statevector_width + text.get_width() / 2,
                           statevector_height + text.get_height()))

def draw_score(screen, classical_score, quantum_score):
    font = resources.Font()

    text = font.player_font.render("Classical Computer", 1, globals.GRAY)
    text_pos = text.get_rect(center=(globals.WINDOW_WIDTH*0.3, globals.WIDTH_UNIT*2))
    screen.blit(text, text_pos)

    text = font.score_font.render(str(classical_score), 1, globals.GRAY)
    text_pos = text.get_rect(center=(globals.WINDOW_WIDTH*0.3, globals.WIDTH_UNIT*8))
    screen.blit(text, text_pos)

    text = font.player_font.render("Quantum Computer", 1, globals.GRAY)
    text_pos = text.get_rect(center=(globals.WINDOW_WIDTH*0.7, globals.WIDTH_UNIT*2))
    screen.blit(text, text_pos)

    text = font.score_font.render(str(quantum_score), 1, globals.GRAY)
    text_pos = text.get_rect(center=(globals.WINDOW_WIDTH*0.7, globals.WIDTH_UNIT*8))
    screen.blit(text, text_pos)

def draw_dashed_line(screen):
    for i in range(10, globals.FIELD_HEIGHT, 2 * globals.WIDTH_UNIT): 
        pygame.draw.rect(
            screen,
            globals.GRAY,
            (globals.WINDOW_WIDTH // 2 - 5, i, 0.5 * globals.WIDTH_UNIT, globals.WIDTH_UNIT),
            0,
        )
