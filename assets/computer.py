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
        if self.paddle.rect.centery - ball.rect.centery > 0:
            self.paddle.rect.y -= self.speed
        else:
            self.paddle.rect.y += self.speed
        
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
        if 88 < ball.rect.x / globals.WIDTH_UNIT < 92:
            if current_time - self.last_measurement_time > globals.MEASUREMENT_COOLDOWN_TIME:
                self.update_after_measurement()
                self.last_measurement_time = pygame.time.get_ticks()
        else:
            self.update_before_measurement()
    
        if pygame.sprite.collide_mask(ball, self.paddles[self.measured_state]):
            ball.bounce() 

    def update_before_measurement(self):
        simulator = qiskit.BasicAer.get_backend("statevector_simulator")
        circuit = self.circuit_grid.model.compute_circuit()
        transpiled_circuit = qiskit.transpile(circuit, simulator)
        statevector = simulator.run(transpiled_circuit, shots=100).result().get_statevector()

        for basis_state, amplitude in enumerate(statevector):
            self.paddles[basis_state].image.set_alpha(abs(amplitude)**2*255)

    def update_after_measurement(self):
        simulator = qiskit.BasicAer.get_backend("qasm_simulator")
        circuit = self.circuit_grid.model.compute_circuit()
        circuit.measure_all()
        transpiled_circuit = qiskit.transpile(circuit, simulator)
        counts = simulator.run(transpiled_circuit, shots=1).result().get_counts()
        self.measured_state = int(list(counts.keys())[0], 2)

        for paddle in self.paddles:
            paddle.image.set_alpha(0)
        self.paddles[self.measured_state].image.set_alpha(255)
