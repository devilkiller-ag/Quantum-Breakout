# colors
WHITE = 255, 255, 255
BLACK = 0, 0, 0
MAGENTA = 255, 0, 255
GRAY = 194, 192, 192

# number of the qubits for the quantum circuit
NUM_QUBITS=3

# Statevector
BASIS_STATES = [
        '|000>',
        '|001>',
        '|010>',
        '|011>',
        '|100>',
        '|101>',
        '|110>',
        '|111>'
    ]

# game dimensions
WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 750
FIELD_HEIGHT = round(WINDOW_HEIGHT * 0.7) # height of pong play field
WIDTH_UNIT = round(WINDOW_WIDTH / 100) # width unit used for scaling the game
# PADDLE_WIDTH = round(FIELD_HEIGHT / 2**NUM_QUBITS) # NOT ACCURATE: Just keep here for future reference
PADDLE_WIDTH = int(round(WINDOW_WIDTH / len(BASIS_STATES)))
PADDLE_HEIGHT = WIDTH_UNIT

STATEVECTOR_WIDTH = int(round(WINDOW_WIDTH / len(BASIS_STATES)))
STATEVECTOR_HEIGHT = int(WINDOW_HEIGHT * 0.62)

# cool down time (in milliseconds) before the next measurement is allowed
MEASUREMENT_COOLDOWN_TIME = 4000

# score to win a game
WIN_SCORE = 1