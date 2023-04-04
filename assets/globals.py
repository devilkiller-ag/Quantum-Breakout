# colors
WHITE = 255, 255, 255
BLACK = 0, 0, 0
MAGENTA = 255, 0, 255
GRAY = 127, 127, 127

# number of the qubits for the quantum circuit
NUM_QUBITS=3

# game dimensions
WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 750
FIELD_HEIGHT = round(WINDOW_HEIGHT * 0.7) # height of pong play field
WIDTH_UNIT = round(WINDOW_WIDTH / 100) # width unit used for scaling the game
PADDLE_HEIGHT = round(FIELD_HEIGHT / 2**NUM_QUBITS)

# cool down time (in milliseconds) before the next measurement is allowed
MEASUREMENT_COOLDOWN_TIME = 4000

# score to win a game
WIN_SCORE = 1