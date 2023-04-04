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

def draw_score(screen, quantum_score):
    font = resources.Font()

    text = font.player_font.render("Score", 1, globals.GRAY)
    text_pos = text.get_rect(center=(globals.WINDOW_WIDTH*0.5, globals.WINDOW_HEIGHT*0.3))
    screen.blit(text, text_pos)

    text = font.score_font.render(str(quantum_score), 1, globals.GRAY)
    text_pos = text.get_rect(center=(globals.WINDOW_WIDTH*0.51, globals.WINDOW_HEIGHT*0.4))
    screen.blit(text, text_pos)