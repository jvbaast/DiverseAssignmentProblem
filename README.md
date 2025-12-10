## Finding a diverse pair of matchings: a bi-objective approach
This repository contains the implementation of the algorithms described in:

>  J. L. E. van Baast, A. López Martinez, F. Spieksma. “Finding a diverse pair of matchings: a bi-objective approach.” Draft. 2026

We implement the exact algorithm and heuristic for solving the diverse assignment problem. We also implement the tests described in Section 4. This paper is just a draft for now, which has not been made available yet.

## Contents
The scripts in this repository contain the following:

#### main.py
This file is used for running the functions implemented in other files. This file should be configured based on you need. There are several options that can be configured and functions that can be run.
1. Configure the instance sizes and types of input files.
2. Generating datasets, this can be commented out if the datasets are already generated.
3. Running the pareto front and timing tests. These can (and should) be commented out if they have already been run. WARNING: running the tests takes a lot of time for larger instances, so only run if necessary.
4. Calculating the Pareto front statistics. The results can be found in the ```pareto/stats``` folder.
5. Plotting the results of the timing tests.

#### algorithm.py
This file contains the implementation of the heuristic described in Section 3 of the paper. We implement one iteration separately and then loop over all values of $k$ in a different function.

#### subroutines.py
Contains the subroutines used by ```Algorithm.py``` including:
1. Solving the cardinality-contrained 2-matching problem.
2. Solving the (unbalanced) transporation problem.
3. Getting the dominating set from a set of points.
4. Finding solutions with minimum assignment weight and diversity weight.

The graph algorithms in these subroutines are implemented using NetworkX [2].

#### exact.py
This file contains the implementation of the exact algorithm. This includes the implementation of the ILP using Gurobi [1] and a recursion to get the Pareto front.

#### pareto_tests.py
This file implements the tests for the relative area measure and the number of solutions. It has two main modes:
1. Preprocessing: This computes the exact and heuristic solutions for the given parameters (input files, instance size, number of iterations). This takes a lot of time, so do not run it unless needed.
2. Statistic calculation: Calculates the results of the tests for the given instances. This can be used to calculate statistics for different subsets of instances. 

#### timing_test.py
This file implements the timing tests. It again has two main modes:
1. Preprocessing: Runs the timing tests for the given parameters. This takes a lot of time, so do not run it unless needed.
2. Statistic calculation: Calculates the results of the tests for the given instances. This can be used to calculate statistics for different subsets of instances. 

#### generate_data.py
This files contains the functions to generate the input files for the tests. There are four types of input files:
1. Disjointness: Specifies the diversity weights such that a solution with maximum diversity weight corresponds to two disjoint matchings.
2. Diversity by distance: The diversity weights are based on how far the indices of two vertices are separated.
3. Two integers: The diversity weights are uniformly sampled from the set $\{-1,1\}$.
4. Random integers: The diversity weights are uniformly sampled from the set $\{k\in\N\mid 0\leq k \leq 100\}$.

#### fileio.py
This file contains the functions for reading and writing solutions, instances and tests results to files.

## Installation
1. Clone this repository
2. Ensure you have Python 3.0 and Pip installed.
3. Install the required packages by running the command ```pip install requirement.txt```
4. Configure and run main.py

## References
[1] Gurobi Optimization, LLC. Gurobi Optimizer Reference Manual. 2025. url: [https://www.
gurobi.com.]()

[2] A. A. Hagberg, D. A. Schult, and P. J. Swart. “Exploring network structure, dynamics, and
function using NetworkX.” In: Proceedings of the 7th Python in Science Conference (SciPy2008).
2008, pp. 11–15.
