import pygame
import qiskit

from . import globals

class Computer:
    def __init__(self):
        pass
    def update(self):
        pass

class ClassicalComputer(Computer):
    def __init__(self, paddle):
        self.paddle = paddle
        self.score = 0
        self.speed = 3

    def update(self, ball):
        if self.paddle.rect.centerx - ball.rect.centerx > 0:
            self.paddle.rect.x -= self.speed
        else:
            self.paddle.rect.x += self.speed
        
        if pygame.sprite.collide_mask(ball, self.paddle):
            ball.bounce()

class QuantumComputer(Computer):
    def __init__(self, quantum_paddles, circuit_grid) -> None:
        self.paddles = quantum_paddles.paddles 
        self.score = 0
        self.circuit_grid = circuit_grid
        self.measured_state = 0
        self.last_measurement_time = pygame.time.get_ticks() - globals.MEASUREMENT_COOLDOWN_TIME

    def update(self, ball):
        current_time = pygame.time.get_ticks()
        # trigger measurement when the ball is close to quantum paddles
        if ball.rect.y > globals.WINDOW_HEIGHT * 0.55:
            # We add measurement cooldown: So that after measurement, it remains in the same state for sometime before re-changing to superposition state according to circuit
            if current_time - self.last_measurement_time > globals.MEASUREMENT_COOLDOWN_TIME:
                self.update_after_measurement()
                self.last_measurement_time = pygame.time.get_ticks()
        else:
            self.update_before_measurement()
    
        if pygame.sprite.collide_mask(ball, self.paddles[self.measured_state]):
            ball.bounce() 

    # To get probabilities of each state before measurement
    def update_before_measurement(self):
        simulator = qiskit.BasicAer.get_backend("statevector_simulator")
        circuit = self.circuit_grid.model.compute_circuit()
        transpiled_circuit = qiskit.transpile(circuit, simulator)
        statevector = simulator.run(transpiled_circuit, shots=100).result().get_statevector()

        # Set the opacity of each paddle equal to the probability of measuring that state
        for basis_state, amplitude in enumerate(statevector):
            self.paddles[basis_state].image.set_alpha(abs(amplitude)**2*255)

    # To measure the state
    def update_after_measurement(self):
        simulator = qiskit.BasicAer.get_backend("qasm_simulator")
        circuit = self.circuit_grid.model.compute_circuit()
        circuit.measure_all()
        transpiled_circuit = qiskit.transpile(circuit, simulator)
        counts = simulator.run(transpiled_circuit, shots=1).result().get_counts()
        self.measured_state = int(list(counts.keys())[0], 2)
        
        # Set all the paddles to transparant
        for paddle in self.paddles:
            paddle.image.set_alpha(0)

        # Then, set only the paddle over the output state to white
        self.paddles[self.measured_state].image.set_alpha(255)
        