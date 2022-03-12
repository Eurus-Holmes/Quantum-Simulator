# Report of Implement a quantum circuit simulator


* [1. Design and evaluation](#1-design-and-evaluation)
  * [Deutsch-Jozsa algorithm](#deutsch-jozsa-algorithm) 
  * [Bernstein-Vazirani algorithm](#bernstein-vazirani-algorithm)
  * [Simon's algorithm](#simons-algorithm)
  * [Grover's algorithm](#grovers-algorithm)
* [2. Instructions](#2-instructions)
  * [Deutsch-Jozsa algorithm](#deutsch-jozsa-algorithm) 
  * [Bernstein-Vazirani algorithm](#bernstein-vazirani-algorithm)
  * [Simon's algorithm](#simons-algorithm)
  * [Grover's algorithm](#grovers-algorithm)
* [3. Cirq](#3-cirq)


## Highlight

- **Particularly comprehensive evaluation and testing**: We included enumerating a range of the length of the input bitstring n and random different Uf functions, as well as customed input n and input function. We measured the standard deviation of runtime and mean run time over 100 repetitions for different randomly generated functions Uf at a range n from 1 to 15. More details are as follow.
- **Code well designed for improved usability or ease of understanding**: Our code includes a unified structure and some general modules: `make_oracle`, `make_dj_circuit`, `run` on the simulator, and `plot` a diagram that maps n to execution time to be reused code from one program to the next. More details are as follow.
- **Vivid diagram display**: We plot diagrams of the execution time as the input n changes, which can show the results more clearly and intuitively.




# 1. Design and evaluation

## Present the design of how you parameterized the solution in n.


## Discuss your effort to test your simulator and present results from the testing.


## What is your experience with scalability as n grows? Present a diagram that maps n to execution time.


# 2. Instructions

## how to provide input


## how to run the program


## how to understand the output



