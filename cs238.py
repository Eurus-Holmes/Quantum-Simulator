import numpy as np
import re


class Simulator:
    def __init__(self, n):
        """
        @param n : number of qubit
        """
        self.n = n
        self.output = 2 ** n
        self.state = np.zeros(self.output, dtype=np.complex128)
        self.state[0] = 1
        self.nstate = np.zeros_like(self.state)
        self.index = np.arange(self.output, dtype=np.uint32)

    def operation(self, gate, target, control=None):
        if gate == "h":
            mask = 1 << (self.n - target[0] - 1)
            self.nstate = (self.state * ((self.index & mask == 0) * 2 - 1) + self.state[
                self.index ^ mask]) / np.sqrt(2.)

        elif gate == "x":
            mask = 1 << (self.n - target[0] - 1)
            self.nstate = self.state[self.index ^ mask]

        elif gate == "t":
            mask = 1 << (self.n - target[0] - 1)
            self.nstate = np.copy(self.state)
            self.nstate[self.index & mask != 0] *= (1 + 1j) / np.sqrt(2.)

        elif gate == "tdg":
            mask = 1 << (self.n - target[0] - 1)
            self.nstate = np.copy(self.state)
            self.nstate[self.index & mask != 0] *= (1 - 1j) / np.sqrt(2.)

        elif gate == "cx":
            mask1 = 1 << (self.n - control[0] - 1)
            mask2 = 1 << (self.n - target[0] - 1)
            self.nstate = np.copy(self.state)
            self.nstate[self.index & mask1 != 0] = self.nstate[self.index[self.index & mask1 != 0] ^ mask2]

        self.state, self.nstate = self.nstate, self.state

    def run(self, circuit):
        for ope in circuit:
            # print(ope)
            self.operation(ope["gate"], ope["targets"], ope["controls"])

    def state_vector(self):
        state_vector = []
        for ind in range(self.output):
            val = self.state[ind]
            state_vector.append(np.around(val, 3))
        return state_vector


def get_num_qubits(qasm_string):
    qasm_list = qasm_string.split('\n')
    qasm_list = qasm_list[4:]
    num_qubits = 0
    for operation in qasm_list:
        if operation == '':
            continue
        ope = operation.split(' ')
        num = re.findall("\d+", ope[1])
        num_list = list(map(int, num))
        # print(num_list)
        max_num = max(num_list)
        num_qubits = max(num_qubits, max_num)
    return num_qubits + 1


def parse_qasm(qasm_string):
    circuit = []
    for qasm in qasm_string.splitlines():
        ope = {'gate': None, 'controls': [], 'targets': []}

        qasm_list = qasm.split()
        if qasm_list[0] in ["OPENQASM", "include", "qreg", "creg"]:
            continue
        if len(qasm_list) == 0:
            continue

        if qasm_list[0] == 'cx':
            qubits = qasm_list[1].split(',')
            qubit0 = int(qubits[0][2:-1])
            qubit1 = int(qubits[1][2:-2])
            ope['gate'] = qasm_list[0]
            ope['controls'].append(qubit0)
            ope['targets'].append(qubit1)
        else:
            qubit = int(qasm_list[1][2:-2])
            ope['gate'] = qasm_list[0]
            ope['targets'].append(qubit)

        circuit.append(ope)

    return circuit


def simulate(qasm_string):
    num_qubits = get_num_qubits(qasm_string)
    # print(num_qubits)
    circuit = parse_qasm(qasm_string)
    # print(circuit)
    my_simulator = Simulator(num_qubits)
    my_simulator.run(circuit)
    state = my_simulator.state_vector()
    # print(state)
    return state
