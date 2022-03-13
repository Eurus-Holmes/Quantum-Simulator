# Report of Implement a quantum circuit simulator


* [1. Design and evaluation](#1-design-and-evaluation)
  * [Present the design of how you parameterized the solution in n](#present-the-design-of-how-you-parameterized-the-solution-in-n) 
  * [Discuss your effort to test your simulator and present results from the testing](#discuss-your-effort-to-test-your-simulator-and-present-results-from-the-testing)
  * [Present a diagram that maps n to execution time](#what-is-your-experience-with-scalability-as-n-grows-present-a-diagram-that-maps-n-to-execution-time)
* [2. Instructions](#2-instructions)
  * [how to provide input](#how-to-provide-input) 
  * [how to run the program](#how-to-run-the-program)
  * [how-to-understand-the-output](#how-to-understand-the-output)


## Highlight

- **Particularly comprehensive evaluation and testing**: We included enumerating a range of the length of the input bitstring n and random different Uf functions, as well as customed input n and input function. We measured the standard deviation of runtime and mean run time over 100 repetitions for different randomly generated functions Uf at a range n from 1 to 15. More details are as follow.
- **Code well designed for improved usability or ease of understanding**: Our code includes a unified structure and some general modules: `make_oracle`, `make_dj_circuit`, `run` on the simulator, and `plot` a diagram that maps n to execution time to be reused code from one program to the next. More details are as follow.
- **Vivid diagram display**: We plot diagrams of the execution time as the input n changes, which can show the results more clearly and intuitively.


You can essentially do matrix multiplication without writing down the matrix.  Just loop through the state vector and implement the operations that the matrix is performing.  There are a lot of bit manipulation tactics that can help you figure out which entries in the state vector to operate on.  For instance, if you want to identify whether the kth qubit is 0 or 1 in the ith entry of the state vector, then you can just call 2^(n-k-1) & i.  


# 1. Design and evaluation

## Present the design of how you parameterized the solution in n

Initialize `Simulator` with parameterized $n$, where $n$ is num of qubits, which is through preprocessing qasm file to get how many qubits that actually need. The `simulate` function takes in a qasm-formatted string and returns a list. The length of list is $2^n$, with each index containing a complex number for each of the $2^n$ possible amplitudes.

```python
def simulate(qasm_string):
    """
    simulate function on the qasm string to compare the results with cirq simulator
    :param qasm_string: qasm-formatted string
    :return: state_vector list
    """
    # preprocessing qasm_string to get how many qubits that actually need
    num_qubits = get_num_qubits(qasm_string)
    # parse qasm_string to generate circuit operation list
    circuit = parse_qasm(qasm_string)
    # initialize simulator with num of qubits
    my_simulator = Simulator(num_qubits)
    # run my simulator to execute the operations in order
    my_simulator.run(circuit)
    # return state_vector list, with a complex number for
    # each of the 2^num_qubits possible amplitudes
    state = my_simulator.state_vector()
    return state
```

## Discuss your effort to test your simulator and present results from the testing


## What is your experience with scalability as n grows? Present a diagram that maps n to execution time


# 2. Instructions

## how to provide input


## how to run the program


## how to understand the output



