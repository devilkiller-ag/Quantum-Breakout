import numpy as np
import pygame
import qiskit

from . import globals, resources, node_types

GRID_WIDTH = 66
GRID_HEIGHT = 66
GATE_TILE_WIDTH = 43
GATE_TILE_HEIGHT = 45
LINE_WIDTH = 1

# navigation
MOVE_LEFT = 1
MOVE_RIGHT = 2
MOVE_UP = 3
MOVE_DOWN = 4


class CircuitGrid(pygame.sprite.RenderPlain):
    """Enables interaction with circuit"""

    def __init__(self, xpos, ypos):
        self.xpos = xpos
        self.ypos = ypos
        self.selected_wire = 0
        self.selected_column = 0
        self.model = CircuitGridModel(globals.NUM_QUBITS, 16)
        self.circuit_grid_background = CircuitGridBackground(self.model)
        self.circuit_grid_cursor = CircuitGridCursor()
        self.gate_tiles = np.empty(
            (self.model.max_wires, self.model.max_columns), dtype=CircuitGridGate
        )

        for row_idx in range(self.model.max_wires):
            for col_idx in range(self.model.max_columns):
                self.gate_tiles[row_idx][col_idx] = CircuitGridGate(
                    self.model, row_idx, col_idx
                )

        pygame.sprite.RenderPlain.__init__(
            self,
            self.circuit_grid_background,
            self.gate_tiles,
            self.circuit_grid_cursor,
        )
        self.update()

    def update(self, *args):
        sprite_list = self.sprites()
        for sprite in sprite_list:
            sprite.update()

        self.circuit_grid_background.rect.left = self.xpos
        self.circuit_grid_background.rect.top = self.ypos

        for row_idx in range(self.model.max_wires):
            for col_idx in range(self.model.max_columns):
                self.gate_tiles[row_idx][
                    col_idx
                ].rect.centerx = self.xpos + GRID_WIDTH * (col_idx + 1.5)
                self.gate_tiles[row_idx][
                    col_idx
                ].rect.centery = self.ypos + GRID_HEIGHT * (row_idx + 1.0)

        self.highlight_selected_node(self.selected_wire, self.selected_column)

    def highlight_selected_node(self, wire_num, column_num):
        self.selected_wire = wire_num
        self.selected_column = column_num
        self.circuit_grid_cursor.rect.left = self.xpos + GRID_WIDTH * (
            self.selected_column + 1
        )
        self.circuit_grid_cursor.rect.top = self.ypos + GRID_HEIGHT * (
            self.selected_wire + 0.5
        )

    def move_to_adjacent_node(self, direction):
        if direction == MOVE_LEFT and self.selected_column > 0:
            self.selected_column -= 1
        elif (
            direction == MOVE_RIGHT
            and self.selected_column < self.model.max_columns - 1
        ):
            self.selected_column += 1
        elif direction == MOVE_UP and self.selected_wire > 0:
            self.selected_wire -= 1
        elif direction == MOVE_DOWN and self.selected_wire < self.model.max_wires - 1:
            self.selected_wire += 1

        self.highlight_selected_node(self.selected_wire, self.selected_column)

    def get_selected_node_gate_part(self):
        return self.model.get_node_gate_part(self.selected_wire, self.selected_column)

    def handle_input(self, key):
        match (key):
            case pygame.K_a:
                self.move_to_adjacent_node(MOVE_LEFT),
            case pygame.K_d:
                self.move_to_adjacent_node(MOVE_RIGHT),
            case pygame.K_w:
                self.move_to_adjacent_node(MOVE_UP),
            case pygame.K_s:
                self.move_to_adjacent_node(MOVE_DOWN),
            case pygame.K_x:
                self.handle_input_x(),
            case pygame.K_y:
                self.handle_input_y(),
            case pygame.K_z:
                self.handle_input_z(),
            case pygame.K_h:
                self.handle_input_h(),
            case pygame.K_SPACE:
                self.handle_input_delete(),
            case pygame.K_c:
                self.handle_input_ctrl(),
            case pygame.K_UP:
                self.handle_input_move_ctrl(MOVE_UP),
            case pygame.K_DOWN:
                self.handle_input_move_ctrl(MOVE_DOWN),
            case pygame.K_LEFT:
                self.handle_input_rotate(-np.pi / 8),
            case pygame.K_RIGHT:
                self.handle_input_rotate(np.pi / 8)

    def handle_input_x(self):
        selected_node_gate_part = self.get_selected_node_gate_part()
        if selected_node_gate_part == node_types.EMPTY:
            circuit_grid_node = CircuitGridNode(node_types.X)
            self.model.set_node(
                self.selected_wire, self.selected_column, circuit_grid_node
            )
        self.update()

    def handle_input_y(self):
        selected_node_gate_part = self.get_selected_node_gate_part()
        if selected_node_gate_part == node_types.EMPTY:
            circuit_grid_node = CircuitGridNode(node_types.Y)
            self.model.set_node(
                self.selected_wire, self.selected_column, circuit_grid_node
            )
        self.update()

    def handle_input_z(self):
        selected_node_gate_part = self.get_selected_node_gate_part()
        if selected_node_gate_part == node_types.EMPTY:
            circuit_grid_node = CircuitGridNode(node_types.Z)
            self.model.set_node(
                self.selected_wire, self.selected_column, circuit_grid_node
            )
        self.update()

    def handle_input_h(self):
        selected_node_gate_part = self.get_selected_node_gate_part()
        if selected_node_gate_part == node_types.EMPTY:
            circuit_grid_node = CircuitGridNode(node_types.H)
            self.model.set_node(
                self.selected_wire, self.selected_column, circuit_grid_node
            )
        self.update()

    def handle_input_delete(self):
        selected_node_gate_part = self.get_selected_node_gate_part()
        if (
            selected_node_gate_part == node_types.X
            or selected_node_gate_part == node_types.Y
            or selected_node_gate_part == node_types.Z
            or selected_node_gate_part == node_types.H
        ):
            self.delete_controls_for_gate(self.selected_wire, self.selected_column)

        if selected_node_gate_part == node_types.CTRL:
            gate_wire_num = self.model.get_gate_wire_for_control_node(
                self.selected_wire, self.selected_column
            )
            if gate_wire_num >= 0:
                self.delete_controls_for_gate(gate_wire_num, self.selected_column)
        elif (
            selected_node_gate_part != node_types.SWAP
            and selected_node_gate_part != node_types.CTRL
            and selected_node_gate_part != node_types.TRACE
        ):
            circuit_grid_node = CircuitGridNode(node_types.EMPTY)
            self.model.set_node(
                self.selected_wire, self.selected_column, circuit_grid_node
            )

        self.update()

    def handle_input_ctrl(self):
        selected_node_gate_part = self.get_selected_node_gate_part()
        if (
            selected_node_gate_part == node_types.X
            or selected_node_gate_part == node_types.Y
            or selected_node_gate_part == node_types.Z
            or selected_node_gate_part == node_types.H
        ):
            circuit_grid_node = self.model.get_node(
                self.selected_wire, self.selected_column
            )
            if circuit_grid_node.ctrl_a >= 0:
                # Gate already has a control qubit so remove it
                orig_ctrl_a = circuit_grid_node.ctrl_a
                circuit_grid_node.ctrl_a = -1
                self.model.set_node(
                    self.selected_wire, self.selected_column, circuit_grid_node
                )

                # Remove TRACE nodes
                for wire_num in range(
                    min(self.selected_wire, orig_ctrl_a) + 1,
                    max(self.selected_wire, orig_ctrl_a),
                ):
                    if (
                        self.model.get_node_gate_part(wire_num, self.selected_column)
                        == node_types.TRACE
                    ):
                        self.model.set_node(
                            wire_num,
                            self.selected_column,
                            CircuitGridNode(node_types.EMPTY),
                        )
                self.update()
            else:
                # Attempt to place a control qubit beginning with the wire above
                if self.selected_wire >= 0:
                    if (
                        self.place_ctrl_qubit(
                            self.selected_wire, self.selected_wire - 1
                        )
                        == -1
                    ):
                        if self.selected_wire < self.model.max_wires:
                            if (
                                self.place_ctrl_qubit(
                                    self.selected_wire, self.selected_wire + 1
                                )
                                == -1
                            ):
                                print("Can't place control qubit")
                                self.display_exceptional_condition()

    def handle_input_move_ctrl(self, direction):
        selected_node_gate_part = self.get_selected_node_gate_part()
        if (
            selected_node_gate_part == node_types.X
            or selected_node_gate_part == node_types.Y
            or selected_node_gate_part == node_types.Z
            or selected_node_gate_part == node_types.H
        ):
            circuit_grid_node = self.model.get_node(
                self.selected_wire, self.selected_column
            )
            if 0 <= circuit_grid_node.ctrl_a < self.model.max_wires:
                # Gate already has a control qubit so try to move it
                if direction == MOVE_UP:
                    candidate_wire_num = circuit_grid_node.ctrl_a - 1
                    if candidate_wire_num == self.selected_wire:
                        candidate_wire_num -= 1
                else:
                    candidate_wire_num = circuit_grid_node.ctrl_a + 1
                    if candidate_wire_num == self.selected_wire:
                        candidate_wire_num += 1
                if 0 <= candidate_wire_num < self.model.max_wires:
                    if (
                        self.place_ctrl_qubit(self.selected_wire, candidate_wire_num)
                        == candidate_wire_num
                    ):
                        print(
                            "control qubit successfully placed on wire ",
                            candidate_wire_num,
                        )
                        if (
                            direction == MOVE_UP
                            and candidate_wire_num < self.selected_wire
                        ):
                            if (
                                self.model.get_node_gate_part(
                                    candidate_wire_num + 1, self.selected_column
                                )
                                == node_types.EMPTY
                            ):
                                self.model.set_node(
                                    candidate_wire_num + 1,
                                    self.selected_column,
                                    CircuitGridNode(node_types.TRACE),
                                )
                        elif (
                            direction == MOVE_DOWN
                            and candidate_wire_num > self.selected_wire
                        ):
                            if (
                                self.model.get_node_gate_part(
                                    candidate_wire_num - 1, self.selected_column
                                )
                                == node_types.EMPTY
                            ):
                                self.model.set_node(
                                    candidate_wire_num - 1,
                                    self.selected_column,
                                    CircuitGridNode(node_types.TRACE),
                                )
                        self.update()
                    else:
                        print(
                            "control qubit could not be placed on wire ",
                            candidate_wire_num,
                        )

    def handle_input_rotate(self, radians):
        selected_node_gate_part = self.get_selected_node_gate_part()
        if (
            selected_node_gate_part == node_types.X
            or selected_node_gate_part == node_types.Y
            or selected_node_gate_part == node_types.Z
        ):
            circuit_grid_node = self.model.get_node(
                self.selected_wire, self.selected_column
            )
            circuit_grid_node.radians = (circuit_grid_node.radians + radians) % (
                2 * np.pi
            )
            self.model.set_node(
                self.selected_wire, self.selected_column, circuit_grid_node
            )

        self.update()

    def place_ctrl_qubit(self, gate_wire_num, candidate_ctrl_wire_num):
        """Attempt to place a control qubit on a wire.
        If successful, return the wire number. If not, return -1
        """
        if (
            candidate_ctrl_wire_num < 0
            or candidate_ctrl_wire_num >= self.model.max_wires
        ):
            return -1
        candidate_wire_gate_part = self.model.get_node_gate_part(
            candidate_ctrl_wire_num, self.selected_column
        )
        if (
            candidate_wire_gate_part == node_types.EMPTY
            or candidate_wire_gate_part == node_types.TRACE
        ):
            circuit_grid_node = self.model.get_node(gate_wire_num, self.selected_column)
            circuit_grid_node.ctrl_a = candidate_ctrl_wire_num
            self.model.set_node(gate_wire_num, self.selected_column, circuit_grid_node)
            self.model.set_node(
                candidate_ctrl_wire_num,
                self.selected_column,
                CircuitGridNode(node_types.EMPTY),
            )
            self.update()
            return candidate_ctrl_wire_num
        else:
            print("Can't place control qubit on wire: ", candidate_ctrl_wire_num)
            return -1

    def delete_controls_for_gate(self, gate_wire_num, column_num):
        control_a_wire_num = self.model.get_node(gate_wire_num, column_num).ctrl_a
        control_b_wire_num = self.model.get_node(gate_wire_num, column_num).ctrl_b

        # Choose the control wire (if any exist) furthest away from the gate wire
        control_a_wire_distance = 0
        control_b_wire_distance = 0
        if control_a_wire_num >= 0:
            control_a_wire_distance = abs(control_a_wire_num - gate_wire_num)
        if control_b_wire_num >= 0:
            control_b_wire_distance = abs(control_b_wire_num - gate_wire_num)

        control_wire_num = -1
        if control_a_wire_distance > control_b_wire_distance:
            control_wire_num = control_a_wire_num
        elif control_a_wire_distance < control_b_wire_distance:
            control_wire_num = control_b_wire_num

        if control_wire_num >= 0:
            for wire_idx in range(
                min(gate_wire_num, control_wire_num),
                max(gate_wire_num, control_wire_num) + 1,
            ):
                print("Replacing wire ", wire_idx, " in column ", column_num)
                circuit_grid_node = CircuitGridNode(node_types.EMPTY)
                self.model.set_node(wire_idx, column_num, circuit_grid_node)


class CircuitGridBackground(pygame.sprite.Sprite):
    """Background for circuit grid"""

    def __init__(self, circuit_grid_model):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.Surface(
            [
                GRID_WIDTH * (circuit_grid_model.max_columns + 2),
                GRID_HEIGHT * (circuit_grid_model.max_wires + 1),
            ]
        )
        self.image.convert()
        self.image.fill(globals.WHITE)
        self.rect = self.image.get_rect()
        pygame.draw.rect(self.image, globals.BLACK, self.rect, LINE_WIDTH)

        for wire_num in range(circuit_grid_model.max_wires):
            pygame.draw.line(
                self.image,
                globals.BLACK,
                (GRID_WIDTH * 0.5, (wire_num + 1) * GRID_HEIGHT),
                (self.rect.width - (GRID_WIDTH * 0.5), (wire_num + 1) * GRID_HEIGHT),
                LINE_WIDTH,
            )


class CircuitGridGate(pygame.sprite.Sprite):
    """Images for nodes"""

    def __init__(self, circuit_grid_model, wire_num, column_num):
        pygame.sprite.Sprite.__init__(self)
        self.circuit_grid_model = circuit_grid_model
        self.wire_num = wire_num
        self.column_num = column_num

        self.update()

    def update(self):
        node_type = self.circuit_grid_model.get_node_gate_part(
            self.wire_num, self.column_num
        )

        if node_type == node_types.H:
            self.image, self.rect = resources.load_image("gates/h_gate.png", -1)
        elif node_type == node_types.X:
            node = self.circuit_grid_model.get_node(self.wire_num, self.column_num)
            if node.ctrl_a >= 0 or node.ctrl_b >= 0:
                if self.wire_num > max(node.ctrl_a, node.ctrl_b):
                    self.image, self.rect = resources.load_image(
                        "gates/not_gate_below_ctrl.png", -1
                    )
                else:
                    self.image, self.rect = resources.load_image(
                        "gates/not_gate_above_ctrl.png", -1
                    )
            elif node.radians != 0:
                self.image, self.rect = resources.load_image("gates/rx_gate.png", -1)
                # self.rect = self.image.get_rect()
                pygame.draw.arc(
                    self.image,
                    globals.MAGENTA,
                    self.rect,
                    0,
                    node.radians % (2 * np.pi),
                    6,
                )
                pygame.draw.arc(
                    self.image,
                    globals.MAGENTA,
                    self.rect,
                    node.radians % (2 * np.pi),
                    2 * np.pi,
                    1,
                )
            else:
                self.image, self.rect = resources.load_image("gates/x_gate.png", -1)
        elif node_type == node_types.Y:
            node = self.circuit_grid_model.get_node(self.wire_num, self.column_num)
            if node.radians != 0:
                self.image, self.rect = resources.load_image("gates/ry_gate.png", -1)
                # self.rect = self.image.get_rect()
                pygame.draw.arc(
                    self.image,
                    globals.MAGENTA,
                    self.rect,
                    0,
                    node.radians % (2 * np.pi),
                    6,
                )
                pygame.draw.arc(
                    self.image,
                    globals.MAGENTA,
                    self.rect,
                    node.radians % (2 * np.pi),
                    2 * np.pi,
                    1,
                )
            else:
                self.image, self.rect = resources.load_image("gates/y_gate.png", -1)
        elif node_type == node_types.Z:
            node = self.circuit_grid_model.get_node(self.wire_num, self.column_num)
            if node.radians != 0:
                self.image, self.rect = resources.load_image("gates/rz_gate.png", -1)
                self.rect = self.image.get_rect()
                pygame.draw.arc(
                    self.image,
                    globals.MAGENTA,
                    self.rect,
                    0,
                    node.radians % (2 * np.pi),
                    6,
                )
                pygame.draw.arc(
                    self.image,
                    globals.MAGENTA,
                    self.rect,
                    node.radians % (2 * np.pi),
                    2 * np.pi,
                    1,
                )
            else:
                self.image, self.rect = resources.load_image("gates/z_gate.png", -1)
        elif node_type == node_types.S:
            self.image, self.rect = resources.load_image("gates/s_gate.png", -1)
        elif node_type == node_types.SDG:
            self.image, self.rect = resources.load_image("gates/sdg_gate.png", -1)
        elif node_type == node_types.T:
            self.image, self.rect = resources.load_image("gates/t_gate.png", -1)
        elif node_type == node_types.TDG:
            self.image, self.rect = resources.load_image("gates/tdg_gate.png", -1)
        elif node_type == node_types.IDEN:
            self.image, self.rect = resources.load_image("gates/iden_gate.png", -1)
        elif node_type == node_types.CTRL:
            if self.wire_num > self.circuit_grid_model.get_gate_wire_for_control_node(
                self.wire_num, self.column_num
            ):
                self.image, self.rect = resources.load_image(
                    "gates/ctrl_gate_bottom_wire.png", -1
                )
            else:
                self.image, self.rect = resources.load_image(
                    "gates/ctrl_gate_top_wire.png", -1
                )
        elif node_type == node_types.TRACE:
            self.image, self.rect = resources.load_image("gates/trace_gate.png", -1)
        elif node_type == node_types.SWAP:
            self.image, self.rect = resources.load_image("gates/swap_gate.png", -1)
        else:
            self.image = pygame.Surface([GATE_TILE_WIDTH, GATE_TILE_HEIGHT])
            self.image.set_alpha(0)
            self.rect = self.image.get_rect()

        self.image.convert()


class CircuitGridCursor(pygame.sprite.Sprite):
    """Cursor to highlight current grid node"""

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = resources.load_image("circuit-grid-cursor.png")
        self.image.convert_alpha()


class CircuitGridModel:
    """Grid-based model that is built when user interacts with circuit"""

    def __init__(self, max_wires, max_columns):
        self.max_wires = max_wires
        self.max_columns = max_columns
        self.nodes = np.empty((max_wires, max_columns), dtype=CircuitGridNode)

    def __str__(self):
        retval = ""
        for wire_num in range(self.max_wires):
            retval += "\n"
            for column_num in range(self.max_columns):
                retval += str(self.get_node_gate_part(wire_num, column_num)) + ", "
        return "CircuitGridModel: " + retval

    def set_node(self, wire_num, column_num, circuit_grid_node):
        self.nodes[wire_num][column_num] = CircuitGridNode(
            circuit_grid_node.node_type,
            circuit_grid_node.radians,
            circuit_grid_node.ctrl_a,
            circuit_grid_node.ctrl_b,
            circuit_grid_node.swap,
        )

    def get_node(self, wire_num, column_num):
        return self.nodes[wire_num][column_num]

    def get_node_gate_part(self, wire_num, column_num):
        requested_node = self.nodes[wire_num][column_num]
        if requested_node and requested_node.node_type != node_types.EMPTY:
            # Node is occupied so return its gate
            return requested_node.node_type
        else:
            # Check for control nodes from gates in other nodes in this column
            nodes_in_column = self.nodes[:, column_num]
            for idx in range(self.max_wires):
                if idx != wire_num:
                    other_node = nodes_in_column[idx]
                    if other_node:
                        if (
                            other_node.ctrl_a == wire_num
                            or other_node.ctrl_b == wire_num
                        ):
                            return node_types.CTRL
                        elif other_node.swap == wire_num:
                            return node_types.SWAP

        return node_types.EMPTY

    def get_gate_wire_for_control_node(self, control_wire_num, column_num):
        """Get wire for gate that belongs to a control node on the given wire"""
        gate_wire_num = -1
        nodes_in_column = self.nodes[:, column_num]
        for wire_idx in range(self.max_wires):
            if wire_idx != control_wire_num:
                other_node = nodes_in_column[wire_idx]
                if other_node:
                    if (
                        other_node.ctrl_a == control_wire_num
                        or other_node.ctrl_b == control_wire_num
                    ):
                        gate_wire_num = wire_idx
                        print(
                            "Found gate: ",
                            self.get_node_gate_part(gate_wire_num, column_num),
                            " on wire: ",
                            gate_wire_num,
                        )
        return gate_wire_num

    def compute_circuit(self):
        qr = qiskit.QuantumRegister(self.max_wires, "q")
        qc = qiskit.QuantumCircuit(qr)

        for column_num in range(self.max_columns):
            for wire_num in range(self.max_wires):
                node = self.nodes[wire_num][column_num]
                if node:
                    if node.node_type == node_types.IDEN:
                        # Identity gate
                        qc.i(qr[wire_num])
                    elif node.node_type == node_types.X:
                        if node.radians == 0:
                            if node.ctrl_a != -1:
                                if node.ctrl_b != -1:
                                    # Toffoli gate
                                    qc.ccx(
                                        qr[node.ctrl_a], qr[node.ctrl_b], qr[wire_num]
                                    )
                                else:
                                    # Controlled X gate
                                    qc.cx(qr[node.ctrl_a], qr[wire_num])
                            else:
                                # Pauli-X gate
                                qc.x(qr[wire_num])
                        else:
                            # Rotation around X axis
                            qc.rx(node.radians, qr[wire_num])
                    elif node.node_type == node_types.Y:
                        if node.radians == 0:
                            if node.ctrl_a != -1:
                                # Controlled Y gate
                                qc.cy(qr[node.ctrl_a], qr[wire_num])
                            else:
                                # Pauli-Y gate
                                qc.y(qr[wire_num])
                        else:
                            # Rotation around Y axis
                            qc.ry(node.radians, qr[wire_num])
                    elif node.node_type == node_types.Z:
                        if node.radians == 0:
                            if node.ctrl_a != -1:
                                # Controlled Z gate
                                qc.cz(qr[node.ctrl_a], qr[wire_num])
                            else:
                                # Pauli-Z gate
                                qc.z(qr[wire_num])
                        else:
                            if node.ctrl_a != -1:
                                # Controlled rotation around the Z axis
                                qc.crz(node.radians, qr[node.ctrl_a], qr[wire_num])
                            else:
                                # Rotation around Z axis
                                qc.rz(node.radians, qr[wire_num])
                    elif node.node_type == node_types.S:
                        # S gate
                        qc.s(qr[wire_num])
                    elif node.node_type == node_types.SDG:
                        # S dagger gate
                        qc.sdg(qr[wire_num])
                    elif node.node_type == node_types.T:
                        # T gate
                        qc.t(qr[wire_num])
                    elif node.node_type == node_types.TDG:
                        # T dagger gate
                        qc.tdg(qr[wire_num])
                    elif node.node_type == node_types.H:
                        if node.ctrl_a != -1:
                            # Controlled Hadamard
                            qc.ch(qr[node.ctrl_a], qr[wire_num])
                        else:
                            # Hadamard gate
                            qc.h(qr[wire_num])
                    elif node.node_type == node_types.SWAP:
                        if node.ctrl_a != -1:
                            # Controlled Swap
                            qc.cswap(qr[node.ctrl_a], qr[wire_num], qr[node.swap])
                        else:
                            # Swap gate
                            qc.swap(qr[wire_num], qr[node.swap])

        return qc


class CircuitGridNode:
    """Represents a node in the circuit grid"""

    def __init__(self, node_type, radians=0.0, ctrl_a=-1, ctrl_b=-1, swap=-1):
        self.node_type = node_type
        self.radians = radians
        self.ctrl_a = ctrl_a
        self.ctrl_b = ctrl_b
        self.swap = swap

    def __str__(self):
        string = "type: " + str(self.node_type)
        string += ", radians: " + str(self.radians) if self.radians != 0 else ""
        string += ", ctrl_a: " + str(self.ctrl_a) if self.ctrl_a != -1 else ""
        string += ", ctrl_b: " + str(self.ctrl_b) if self.ctrl_b != -1 else ""
        return string
