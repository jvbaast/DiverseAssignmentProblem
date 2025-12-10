### File implementing the approximation algorithm described in the paper
import subroutines
import numpy as np

# Runs the approximation algorithm in a (G, D, k) instance
def run_algorithm(G, D, n, k):

    # Solve k-cardinality 2-matching
    two_matching = subroutines.solve_k_card_2_matching(D, k)

    # Make a transportation from 2-matching to L
    H = np.zeros((n, n*n))
    supplies = np.zeros(n)
    demands = np.zeros(n*n)

    # Create auxiliary graph weights and demands
    for i in range(n):
        supplies[i] = 1 # Supply is always 1
        for j in range(n):
            for k in range(j,n):

                # Set weight of edges
                H[i][j*n + k] = G[i][j] + G[i][k]

                # Set demand to demand = x_e
                demands[j*n + k] = two_matching.get((j,k), 0)

    flow = subroutines.solve_transportation(H, supplies, demands) 

    # Create a matching from the transportation
    edge_matching = []
    for i in range(n):
        for j in range(n, n*n+n):
            if flow[i][j] > 0:
                edge_matching += [(i,((j-n) // n, (j-n) % n), flow[i][j])]

    # Matching remaining nodes using a transportation
    supplies = 2 * np.ones(n)
    demands = 2 * np.ones(n)

    assignment = np.zeros((n,n))
    for match in edge_matching:

        # Set supply = 
        supplies[match[0]] = 0

        # Set demand = 2 - x_e 
        demands[match[1][0]] -= match[2]
        demands[match[1][1]] -= match[2]

        # Assign nodes based on the earlier matching
        assignment[match[0]][match[1][0]] += match[2]
        assignment[match[0]][match[1][1]] += match[2]

    flow = subroutines.solve_transportation(G, supplies, demands)

    # Make matching based on transportation
    matching = []
    for i in range(n):
        for j in range(n, 2*n):
            if flow[i][j] > 0:
                matching += [(i,j-n,flow[i][j])]

    # Make assignment based on matching
    for match in matching:
        assignment[match[0]][match[1]] += match[2]

    # Calculate cost of solution
    cost = 0
    for i in range(n):
        for j in range(n):
            cost += assignment[i][j] * G[i][j]

    # Calculate diversity of solution
    diversity = 0
    for i in range(n):
        r = []
        for j in range(n):
            if assignment[i][j] > 0:
                r += [j] * int(assignment[i][j])
        diversity += D[r[0]][r[1]]

    return assignment, cost, diversity

# Calculate n points using the approximate algorithm
def get_algorithm_points(G, D, n):
    result = []
    for i in range(n+1):
        ass, cost, div = run_algorithm(G, D, n, i)
        result += [(cost, div)]
    dominating_set = subroutines.get_dominating_set(result)
    return dominating_set