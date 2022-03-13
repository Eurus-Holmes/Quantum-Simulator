import numpy as np
import re


class Simulator:
    """
    implement a quantum circuit simulator for a subset of QASM programs.
    a subset of QASM programs that is defined by the following grammar:
    (Program) p::= OPENQASM 2.0;
                   include "qelib1.inc";
                   qreg q[ n];
                   creg c[ n];
                   s∗

    (Statement) s::= h q[ n];
                  |  x q[ n];
                  |  t q[ n];
                  |  tdg q[ n];
                  |  cx q[ n]; q[ n];

    We have 14 benchmark programs that follow the above grammar:
            miller_11.qasm              3 qubits 54 lines
            decod24-v2_43.qasm          4 qubits 56 lines
            one-two-three-v3_101.qasm   5 qubits 74 lines
            hwb5_53.qasm                6 qubits 1,340 lines
            alu-bdd_288.qasm            7 qubits 88 lines
            f2_232.qasm                 8 qubits 1,210 lines
            con1_216.qasm               9 qubits 958 lines
            mini_alu_305.qasm           10 qubits 177 lines
            wim_266.qasm                11 qubits 990 lines
            cm152a_212.qasm             12 qubits 1,225 lines
            squar5_261.qasm             13 qubits 1,997 lines
            sym6_316.qasm               14 qubits 274 lines
            rd84_142.qasm               15 qubits 347 lines
            cnt3-5_179.qasm             16 qubits 179 lines
    """

    def __init__(self, n):
        """
        initialize simulator with parameterized n
        :param n : num of qubits
        """
        self.n = n
        # expected output state_vector length: 2^num_qubits
        self.output = 2 ** n
        # Each index in the list is representative if one of the possible basis states in the state vector.
        # The indices use big endian ordering for the qubits.
        # reference: https://quantumai.google/reference/python/cirq/sim/StateVectorTrialResult#state_vector
        self.index = np.arange(self.output, dtype=np.uint32)
        # the output state_vector list
        self.state = np.zeros(self.output, dtype=np.complex128)
        # initial state: |0^n>, so state[index=0] is 1
        self.state[0] = 1
        # a copy of state_vector list
        self.state_copy = np.zeros_like(self.state)

    def operation(self, gate, target, control=None):
        """
        implement each gate with bit manipulation to the target and control qubit
        :param gate: operations of gate, including h|x|t|tdg|cx according to the grammar
        :param target: target qubit index
        :param control: control qubit index
        :return: the state_vector list after applying gates to the target and control qubit
        """
        if gate == "h":
            mask = 1 << (self.n - target[0] - 1)
            self.state_copy = (self.state * ((self.index & mask == 0) * 2 - 1) + self.state[
                self.index ^ mask]) / np.sqrt(2)

        elif gate == "x":
            mask = 1 << (self.n - target[0] - 1)
            self.state_copy = self.state[self.index ^ mask]

        elif gate == "t":
            mask = 1 << (self.n - target[0] - 1)
            self.state_copy = np.copy(self.state)
            self.state_copy[self.index & mask != 0] *= (1 + 1j) / np.sqrt(2)

        elif gate == "tdg":
            mask = 1 << (self.n - target[0] - 1)
            self.state_copy = np.copy(self.state)
            self.state_copy[self.index & mask != 0] *= (1 - 1j) / np.sqrt(2)

        elif gate == "cx":
            mask1 = 1 << (self.n - control[0] - 1)
            mask2 = 1 << (self.n - target[0] - 1)
            self.state_copy = np.copy(self.state)
            self.state_copy[self.index & mask1 != 0] = self.state_copy[self.index[self.index & mask1 != 0] ^ mask2]

        self.state, self.state_copy = self.state_copy, self.state

    def run(self, circuit):
        """
        run simulator through simulate circuit operation,
        according to the circuit parsed from the function: parse_qasm(qasm_string),
        the main loop executes the operations in order
        :param circuit: circuit parsed from qasm_string, with a dictionary list form,
        such as: {'gate': 'cx', 'controls': [7], 'targets': [9]}
        """
        for ope in circuit:
            # print(ope)
            self.operation(ope["gate"], ope["targets"], ope["controls"])

    def state_vector(self):
        """
        the output state_vector list,
        the list is 2^num_qubits length,
        with each index containing a complex number.
        """
        state_vector = []
        for ind in range(self.output):
            val = self.state[ind]
            state_vector.append(np.around(val, 3))
        return state_vector


def get_num_qubits(qasm_string):
    """
    preprocessing qasm_string to get how many qubits that actually need
    :param qasm_string: qasm-formatted string
    :return: num of qubits that actually need
    """
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
    """
    parse qasm_string to generate circuit operation list
    :param qasm_string: qasm-formatted string
    :return: circuit parsed from qasm_string, with a dictionary list form,
    such as: {'gate': 'cx', 'controls': [7], 'targets': [9]}
    """
    circuit = []
    for qasm in qasm_string.splitlines():
        ope = {'gate': None, 'controls': [], 'targets': []}

        qasm_list = qasm.split()
        # skip header of qasm
        if qasm_list[0] in ["OPENQASM", "include", "qreg", "creg"]:
            continue
        # skip empty lines
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
    """
    simulate function on the qasm string to compare the results with cirq simulator
    :param qasm_string: qasm-formatted string
    :return: state_vector list
    """
    # preprocessing qasm_string to get how many qubits that actually need
    num_qubits = get_num_qubits(qasm_string)
    # print(num_qubits)

    # parse qasm_string to generate circuit operation list
    circuit = parse_qasm(qasm_string)
    # print(circuit)

    # initialize simulator with num of qubits
    my_simulator = Simulator(num_qubits)
    # run my simulator to execute the operations in order
    my_simulator.run(circuit)

    # return state_vector list, with a complex number for
    # each of the 2^num_qubits possible amplitudes
    state = my_simulator.state_vector()
    # print(state)
    return state
