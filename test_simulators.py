import sys
import numpy as np
import cirq
from cirq.contrib.qasm_import import circuit_from_qasm
from pathlib import Path
import time
import matplotlib.pyplot as plt

# Import your simulate function here.
# cs238 can be a file, a folder with an __init__.py file,
from cs238 import simulate
from cs238 import get_num_qubits


def cirq_simulate(qasm_string: str) -> list:
    """Simulate a qasm string

    Args:
        qasm_string: a string following the qasm format

    Returns:
        statevector: a list, with a complex number for
            each of the 2^num_qubits possible amplitudes
            Ordered big endian, see:
        quantumai.google/reference/python/cirq/sim/StateVectorTrialResult#state_vector
    """

    circuit = circuit_from_qasm(qasm_string)
    result = cirq.Simulator().simulate(circuit)
    statevector = list(np.around(result.state_vector(), 3))
    return statevector


def compare(state_vector, cirq_state_vector):
    """Our comparison function for your grade

    Args:
        state_vector: your state vector amplitude list
        cirq_state_vector: cirq's state vector amplitude list

    Returns:
        Some value influencing your grade, subject to change :)
    """

    return np.all(np.isclose(state_vector, cirq_state_vector))


# get the directory of qasm files and make sure it's a directory
qasm_dir = Path(sys.argv[1])
assert qasm_dir.is_dir()

total = 0
correct = 0
my_time_list = []
cirq_time_list = []
ns = []

# iterate the qasm files in the directory
for qasm_file in qasm_dir.glob("**/*.qasm"):
    total += 1
    # read the qasm file
    with open(qasm_file, "r") as f:
        qasm_string = f.read()
    print(qasm_file)

    num_qubits = get_num_qubits(qasm_string)
    start1 = time.time()
    # run your simulate function on the qasm string
    state_vector = simulate(qasm_string)
    end1 = time.time()
    my_time = end1-start1
    print(f"my simulator finished in {my_time} seconds")
    # print("state_vector:", state_vector)
    # print('\n')
    # run cirq's simulator on the qasm string
    start2 = time.time()
    cirq_state_vector = cirq_simulate(qasm_string)
    end2 = time.time()
    cirq_time = end2-start2
    print(f"cirq simulator finished in {cirq_time} seconds")
    # print(cirq_state_vector)
    # print('\n')
    # compare the results!
    print(compare(state_vector, cirq_state_vector))
    flag = compare(state_vector, cirq_state_vector)
    if flag:
        correct += 1

    ns.append(num_qubits)
    my_time_list.append(my_time)
    cirq_time_list.append(cirq_time)

print("\nTotal {} benchmark, {} are correct, grade is {:.2f}%!".format(total, correct, (correct/total*100)))


# plot a diagram that maps n to execution time
# print(ns)
# print(my_time_list)
new = zip(*sorted(zip(ns, my_time_list, cirq_time_list)))
x_axis, y1_axis, y2_axis = [list(x) for x in new]
# print("num of qubits: ", x_axis)
# print("my simulator time: ", y1_axis)
# print("cirq simulator time: ", y2_axis)
fig = plt.figure()
plt.plot(x_axis, y1_axis, "o-", label="my simulator")
plt.plot(x_axis, y2_axis, "*-", label="cirq simulator")
plt.xlabel("num of qubits")
plt.ylabel("simulator runtime (seconds)")
plt.legend()
plt.savefig("simulator_time.png")
plt.show()
